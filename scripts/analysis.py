###############################################################################
# File  : thesiscode/scripts/analysis.py
# Author: madicken
# Date  : Tue Mar 14 14:05:05 2017
#
# <+Description+>
###############################################################################

from __future__ import (division, absolute_import, print_function, )

#-----------------------------------------------------------------------------#

import numpy as np
import h5py
from mcnpoutput import TrackLengthTally
from plotting_utils import ( names, energy_histogram )
from matplotlib import pyplot as plt
import seaborn as sns
import json

###############################################################################

class MCNPOutput(object):
    def __init__(self, outputlocation, tallynumber='44'):
        self.outputlocation = str(outputlocation)
        self.title = self.outputlocation
        self.tallynumber = tallynumber
        pass

    def get_tally_data(self):
        output_init = TrackLengthTally(self.outputlocation, self.tallynumber)
        output_fom = output_init.get_fom_data()
        output_tally = output_init.get_tally_result()
        output_timing = output_init.get_timing_data()

        output_container = {'timing' : output_timing,
                            'fom_trends' : output_fom,
                            'tally_data' : output_tally}

        return output_container

#-----------------------------------------------------------------------------#

class TimingOutput(object):
    def __init__(self, timingfilelocation):
        self.timingfile = str(timingfilelocation)
        pass

    def get_timing_data(self, extraopts=['strings']):
        timingfile = open(self.timingfile)
        tf = json.loads(timingfile.read())

        defaults = [
              'mix_mats',
              'map_cells',
              'Quantifying anisotropy with six anisotropy metrics.',
              ]

        ignore_keys = defaults + extraopts

        timing_keys = tf.keys()
        full_det_time = np.sum(tf.values())
        newtime = full_det_time
        for option in ignore_keys:
            if option not in timing_keys:
                print('%s not in timing output. ' %option
                      +  ' Not including it in calculation')
            else:
                print('%s found in timing output. ' %option
                      +  ' Subtracting value from total deterministic'
                      +  ' runtime')

                newtime = newtime-tf[option]

        timing_data = {
                'full_deterministic_time': full_det_time,
                'adjusted_deterministic_time': newtime,
                'excluded_keys' : ignore_keys,
                'all_timing_keys': timing_keys,
                'units':'seconds'
                }

        return timing_data



#-----------------------------------------------------------------------------#

class H5Output(object):
    def __init__(self, outputlocation):
        self.outputlocation = str(outputlocation)
        pass

    def get_all_data(self):
        f=h5py.File('%s' %(self.outputlocation), 'r')

        return all_data

    def get_datanames(self):
        f = h5py.File('%s' %(self.outputlocation),'r')
        metric_names = f.keys()
        energy_groups = f[metric_names[0]].keys()

        names = {'metric_names' : metric_names,
                 'energy_groups' : energy_groups}

        return names

    def get_dataset_by_metric(self, metric_name, num_samples = 1500,
                             flatten_data=True):
        ''' This function returns a dict with the names of eeach energy group
        and a matrix of data corresponding to a sample of anisotropy data (n
        samples) for a specified metric name.  '''

        full_dataset = self.get_data_by_metric(metric_name,
                flatten_data=flatten_data)
        full_data = full_dataset['data']

        size = np.shape(full_data)
        num_groups = size[-1]

        data = np.zeros(num_samples)
        for group in np.arange(num_groups):
            dataset = full_data[:,group]
            newdata = np.random.choice(dataset,num_samples)
            data = np.column_stack((data,newdata))

        data = data[:,1:]

        metricdata = {'names' : full_dataset['names'],
                     'data' : data,
                     'description': '%s count sample of ' %(num_samples)
                           + 'anisotropy data for all energy groups, %s'
                     %(metric_name)}

        return metricdata


    def get_data_by_metric(self, metric_name, flatten_data=True):
        '''This function returns a dict with the names of each group and a
        matrix of data corresponding to the anisotropy data (groupwise) for a
        specifed metric name If flatten_data is set to False, then the data
        matrix returned in the dict will have dimensions of (groups, x, y, z),
        else it will be (groups, x*y*z). Because this function is used
        primarily for plotting, the dimensionality of the flattened array is
        desired. '''

        # open the file as readonly
        f=h5py.File('%s' %(self.outputlocation), 'r')


        # set up empty arrays for data storage before loading it in
        matrix_size = f['%s' %metric_name]['group_000'].size
        data = np.zeros([matrix_size])
        names = []

        # loop through the data in the hdf5 file and load it in
        for group in f['%s' %metric_name]:
            subdata = f['%s' %metric_name][group][:].flatten()
            data = np.row_stack((data,subdata))
            names.append(group)

        # Rotate the matrix for plotting optimization
        data = np.transpose(data)

        # clear out the row of zeros that appears from row_stack
        data = data[:,1:]

        metricdata = {'names' : names,
                     'data' : data,
                     'description': 'anisotropy data for all energy groups, %s'
                     %metric_name}

        return metricdata

    def get_data_by_energy(self, group_number, flatten_data=True):
        '''This function will return a dict of the names of each metric that
        have been aquired and an array of data corresponding to the anisotropy
        data for each metric given a specified energy group number. If
        flatten_data is set to False, then the data matrix will have
        dimensions of (no. metrics, x, y, z), else it will be (no. metrics,
        x*y*z) '''

        # open the file as readonly
        f=h5py.File('%s' %(self.outputlocation), 'r')

        # set up empty arrays for data storage before loading it in
        matrix_size = f['forward_anisotropy']['group_000'].size
        data = np.zeros([matrix_size])
        names = []

        if type(group_number) == int:
            group_number = 'group_%03d' %group_number
        elif type(group_number) == unicode or str:
            group_number = group_number
        else:
            print('group number is not a recognized type')

        # loop through the data in the hdf5 file and load it in
        for metric in f:
            subdata = f[metric][group_number][:].flatten()
            data = np.row_stack((data,subdata))
            names.append(metric)

        # Rotate the matrix for plotting optimization
        data = np.transpose(data)

        # clear out the row of zeros that appears from row_stack
        data = data[:,1:]

        groupdata = {'names': names,
                      'data': data,
                      'description':'anisotropy data for all metrics, energy %s'
                                     %group_number}

        return groupdata

    def get_dataset_by_energy(self, group_number, num_samples = 1500,
                             flatten_data=True):
        ''' This function returns a dict with the names of eeach energy group
        and a matrix of data corresponding to a sample of anisotropy data (n
        samples) for a specified metric name.  '''

        full_dataset = self.get_data_by_energy(group_number,
                flatten_data=flatten_data)
        full_data = full_dataset['data']

        if type(group_number) == int:
            group_number = 'group_%03d' %group_number
        elif type(group_number) == unicode or str:
            group_number = group_number
        else:
            print('group number is not a recognized type')

        size = np.shape(full_data)
        num_metrics = size[-1]

        data = np.zeros(num_samples)
        for metric in np.arange(num_metrics):
            dataset = full_data[:,metric]
            newdata = np.random.choice(dataset,num_samples)
            data = np.column_stack((data,newdata))

        data = data[:,1:]

        groupdata = {'names' : full_dataset['names'],
                     'data' : data,
                     'description': '%s count sample of ' %(num_samples)
                           + 'anisotropy data for all metrics, energy %s'
                     %(group_number)}

        return groupdata

    def get_data_statistics(self):
        '''This function gets the average value and standard deviation for each
        metric by energy group and returns two matrices: one with dims
        (metric*no.groups) corresponding to the averages, and the other for the
        standard deviations. Two lists will also be outputted corresponding to
        the metric names and the group numbers'''

        # open the file as readonly
        f=h5py.File('%s' %(self.outputlocation), 'r')

        # set up the labelling lists
        metric_names = f.keys()
        group_numbers = f['forward_anisotropy'].keys()

        # set up empty arrays for data storage before loading it in
        no_metrics = len(metric_names)
        no_groups = len(group_numbers)
        data = np.zeros([no_metrics, no_groups, 4])

        # now set up the loops to calculate metrics on subsets of data
        for metric in metric_names:
            metric_location = metric_names.index(metric)
            for group in group_numbers:
                group_location = group_numbers.index(group)

                # pull the chunk of data associated with metric and group from
                # the file.
                data_chunk = f[metric][group][:]

                # calculate the statistics on the data chunk and put them into
                # an array.
                mean = np.mean(data_chunk)
                median = np.median(data_chunk)
                std = np.std(data_chunk)
                var = np.var(data_chunk)
                stats = np.array([mean, median, std, var])

                data[metric_location,group_location,:] = stats

        statistics = ['mean', 'median', 'standard deviation', 'variance']

        stats_container = {'metrics' : metric_names,
                           'group numbers' : group_numbers,
                           'statistics' : statistics,
                           'data' : data}

        return stats_container


#-----------------------------------------------------------------------------#

class DenovoOutput(object):
    def __init__(self, outputdirectory):
        self.outputdirectory = str(outputdirectory)
        pass

    def get_timing_data(self):
        pass

    def get_statistical_info(self):
        pass


#-----------------------------------------------------------------------------#

class AnisotropyAnalysis(object):
    def __init__(self):
        pass

#-----------------------------------------------------------------------------#

class FOMAnalysis(object):
    ''' This class has the options to calculate simple FoM data for a single
    run.  '''
    def __init__(self, MC_output_file, tallynumber, deterministic_timing_file,
            datasavepath=''):
        self.mc_output_file = MC_output_file
        self.tallynumber = tallynumber
        self.det_timing_file = deterministic_timing_file

        self.det_timingdata = TimingOutput(self.det_timing_file).get_timing_data()
        self.mc_data = MCNPOutput(self.mc_output_file,
                        tallynumber=self.tallynumber).get_tally_data()

        self.all_foms = {}

        if datasavepath:
            self.savepath = datasavepath
        else:
            import os
            path1 = os.path.dirname(MC_output_file)
            path2 = os.path.join(path1, '../analysis/')
            path2 = os.path.normpath(path2)
            self.savepath = path2
        pass

    def print_tally_convergence(self, printtype='tex'):
        self.gettallyframe(self.mc_data['fom_trends'], index='nps')

        pass

    def get_tallyframe(datadict, index=''):
        if index:
            ind_digits = [int(num) for num in datadict[index]]
            tallyframe = pd.DataFrame(datadict, index=ind_digits)
        else:
            tallyframe = pd.DataFrame(datadict)

        return tallyframe


    def plot_fom_convergence(self):
        xdata = self.mc_data['fom_trends']['nps']
        ydata = self.mc_data['fom_trends']['fom']
        x_label = 'Number of Source Particles'
        y_label = 'Figure of Merit'
        plt_title = 'Figure of Merit Convergence'
        plt_name = 'fom_converge'
        self.generic_scatterplot(xdata, ydata, self.savepath, title=plt_title,
                xlabel=x_label, ylabel=y_label, plot_name=plt_name)
        pass

    def generate_fom_table(self):

        # check to see if foms have been generated
        if not self.all_foms:
            all_foms = self.calculate_all_foms()
        else:
            all_foms = self.all_foms

        pass

    def generic_scatterplot(self, xdata, ydata, savepath, title='title',
            xlabel='xlabel', ylabel='ylabel', plot_name='generic'):
        sns.set_style('ticks',
                      {'ytick.direction': u'in',
                       'xtick.direction': u'in'})
        pal = sns.cubehelix_palette()
        x=xdata
        y=ydata
        plt.scatter(x,y, s=26, c=pal[3])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig('%s/%s.png' %(savepath,plot_name), hbox_inches='tight')

    def calculate_all_foms(self):

        std_fom = self.mc_data['fom_trends']['fom'][-1]
        std_fom_mean = self.mc_data['fom_trends']['mean'][-1]
        std_fom_err = self.mc_data['fom_trends']['error'][-1]
        std_fom_pcount = self.mc_data['fom_trends']['nps'][-1]

        std_fom_time = self.mc_data['timing']['mcrun_time']['time']
        det_time = self.det_timingdata['adjusted_deterministic_time']

        # make sure units match between files

        det_units = self.det_timingdata['units']
        mc_units = self.mc_data['timing']['mcrun_time']['units']
        if det_units == 'seconds' and mc_units == 'minutes':
            det_time = det_time/60.0
        else:
            print('The units for these timing files are different from expected'
                  ' vals. det units are %s and mc units are %s' %(det_units, mc_units)
                    )

        total_time = std_fom_time + det_time

        time_data = {'mc_time': std_fom_time,
                     'det_time' : det_time,
                     'total_time' : total_time,
                     'units': mc_units}

        total_err = self.mc_data['tally_data']['tally_total_relative_error']
        max_err = self.mc_data['tally_data']['relative_error'].max()
        min_err = self.mc_data['tally_data']['relative_error'].min()

        dat1 = self.make_fom_dict(std_fom_err, std_fom_time)
        dat2 = self.make_fom_dict(max_err, std_fom_time)
        dat3 = self.make_fom_dict(min_err, std_fom_time)
        dat4 = self.make_fom_dict(total_err, total_time)
        dat5 = self.make_fom_dict(max_err, total_time)
        dat6 = self.make_fom_dict(min_err, total_time)

        fom_results = {
                   'fom_mc': dat1,
                   'fom_max': dat2,
                   'fom_min': dat3,
                   'fom_mc_det':dat4,
                   'fom_max_det':dat5,
                   'fom_min_det':dat6,
                   'particle_count': std_fom_pcount,
                   'times_used' : time_data,
                   }

        self.all_foms = fom_results

        return fom_results

    def make_fom_dict(self,err,time):

        figure_of_merit = np.divide(1,(err**2)*time)

        return {
                'time': time,
                'relative_error' : err,
                'FOM' : figure_of_merit,
                }

#-----------------------------------------------------------------------------#

###############################################################################
# end of thesiscode/scripts/analysis.py
###############################################################################
