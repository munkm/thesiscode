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
from plotting_utils import ( violinbyenergy, stripbygroup, violinbygroup, names,
                          energy_histogram )
from matplotlib import pyplot as plt
import seaborn as sns
###############################################################################

class MCNPOutput(object):
    def __init__(self, outputlocation, tallynumber='44'):
        self.ouputlocation = str(outputlocation)
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

class H5Output(object):
    def __init__(self, outputlocation):
        self.outputlocation = str(outputlocation)
        pass

    def get_all_data(self):
        f=h5py.File('%s' %(self.outputlocation), 'r')

        return all_data

    def get_data_by_group(self, metric_name, flatten_data=True):
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

        groupdata = {'names' : names,
                     'data' : data,
                     'description': 'anisotropy data for all energy groups, metric %s'
                     %metric_name}

        return groupdata

    def get_data_by_metric(self, group_number, flatten_data=True):
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

        # loop through the data in the hdf5 file and load it in
        for metric in f:
            subdata = f[metric]['group_%03d' %group_number][:].flatten()
            data = np.row_stack((data,subdata))
            names.append(metric)

        # Rotate the matrix for plotting optimization
        data = np.transpose(data)

        # clear out the row of zeros that appears from row_stack
        data = data[:,1:]

        metricdata = {'names': names,
                      'data': data,
                      'description':'anisotropy data for all metrics, group %d' %group_number}

        return metricdata

    def get_paths(self):
        pass

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
    def __init__(self):
        pass

    def plot_fom_data(self):
        return

    def calculate_all_foms(mcnpdict,denovodict):

        fom_results = {'fom_mc': fig1,
                   'fom_max': fig2,
                   'fom_min': fig3,
                   'fom_mc_adj':fig4,
                   'fom_max_adj':fig5,
                   'fom_min_adj':fig6}
        return fom_results

#-----------------------------------------------------------------------------#

###############################################################################
# end of thesiscode/scripts/analysis.py
###############################################################################
