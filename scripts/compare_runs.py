###############################################################################
# File  : thesiscode/scripts/compare_runs.py
# Author: madicken
# Date  : Tue Apr 18 09:44:11 2017
#
# <+Description+>
###############################################################################
from __future__ import (division, absolute_import, print_function, )
#-----------------------------------------------------------------------------#
import numpy as np

from single_run import Single_Run
from analysis_utils import format_logger
from plotting_utils import energy_histogram, styles
import logging
import os
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pickle

###############################################################################

class Compare_Runs(object):
    def __init__(self, cadisanglefolder='', cadisfolder='', analogfolder='',
            problem_name=''):

        # initialize logger
        cadisanglefolder = os.path.expanduser(cadisanglefolder)

        logger = logging.getLogger("analysis")

        if os.path.isdir(cadisanglefolder):
            dirpath = cadisanglefolder+'/analysis_compare'
            if os.path.isdir(dirpath):
                logfile = '%s/compare_analysis.log' %dirpath
            else:
                os.makedirs(dirpath)
                logfile = '%s/compare_analysis.log' %dirpath
            self.analysis_dir = dirpath
        else:
            logger.error('%s is not a known directory' %cadisanglefolder)

        if logger.handlers:
            logger = logger
        else:
            logfile = '%s/compare_analysis.log' %dirpath
            logger = format_logger("analysis", logfile)

        logger.info("Initiated %s analysis" %__name__)

        self.cadisangledata = self.get_data(cadisanglefolder, 'cadisangle')
        self.cadisdata = self.get_data(cadisfolder, 'cadis')
        self.analogdata = self.get_data(analogfolder, 'analog')
        if not self.analysis_dir:
            self.analysis_dir = self.cadisangledata.directories['analysis_directory']
        self.problem_name = problem_name

        self.saveformat = 'txt'
        pass

    def get_data(self, folderpath, method_type=''):
        '''
        convenience function to obtain single_run data for a given method
        folderpath and method_type. Returns single_run object for that
        analysis.
        '''

        if folderpath:
            data = Single_Run(folderpath, method_type=method_type)
            data.do_single_analysis()
        else:
            data = None

        return data

    def plot_tally_result(self, savepath=None):
        '''
        Plots a histogram of the tally result for all methods.
        '''
        self.plot_compare(compare_type='tallied_result',
                y_label='Tally Result', title='%s comparison of tally result'
                %self.problem_name, savepath=savepath)
        return

    def plot_tally_error(self, savepath=None):
        '''
        Plots a histogram of the tally relative error for each method.
        '''
        self.plot_compare(compare_type='relative_error',
                y_label='Tally Relative Error',
                title='%s comparison of tally relative error'
                %self.problem_name, savepath=savepath)
        return

    def plot_compare(self, compare_type='tallied_result',
                     savepath=None, y_label='', title=''):
        '''
        Plotting function to plot multiple energy histograms on a single
        figure.
        '''
        logger = logging.getLogger("analysis.compare")

        # gets the tally data for each method.
        energy_groups = \
            self.cadisangledata.MCNP_data['tally_data']['energy_groups']
        cadang = self.cadisangledata.MCNP_data['tally_data'][compare_type]
        cad = self.cadisdata.MCNP_data['tally_data'][compare_type]
        analog = self.analogdata.MCNP_data['tally_data'][compare_type]

        # check to see if results are identical. Modify them with a warning log
        # message if they do.
        if cad.all() == cadang.all():
            logger.warning("""The results for cadis and cadisangle seem to be
                    identical. Plotting cadis at 1.05 higher than actual
                    results.""")
            cad = cad*1.05
        if analog.all() == cadang.all():
            logger.warning(""" The results for analog and cadisangle seem to be
                    identical. Plotting analog at 1.10 higher than actual
                    results.""")
            analog = analog*1.10

        # open figure object
        fig = plt.figure()

        # plot a histogram on the figure for each method type.
        energy_histogram(energy_groups, cadang, None,
                **styles[self.cadisangledata.method_type])
        energy_histogram(energy_groups, cad, None,
                **styles[self.cadisdata.method_type])
        energy_histogram(energy_groups, analog, None,
                **styles[self.analogdata.method_type])

        plt.legend()

        if title:
            plt.title('%s' %title)
        elif self.problem_name:
            plt.title('%s' %problem_name)

        if y_label:
            plt.ylabel('%s' %y_label)
        else:
            plt.ylabel('%s' %compare_type)

        if savepath is not None:
            plt.savefig('%s' %(savepath), hbox_inches='tight')
            plt.close(fig)
        else:
            return fig
        return

    def make_table(self, framename):
        '''
        Merges pandas dataframes from results into a super-dataframe with
        results from all methods. Returns dataframe.
        '''
        logger = logging.getLogger("analysis.compare")
        logger.debug('composite frame of %s being created' %framename)

        cad = self.cadisdata.frames[framename].transpose()
        cad_label = self.cadisdata.method_type
        cadom = self.cadisangledata.frames[framename].transpose()
        cadom_label = self.cadisangledata.method_type
        analog = self.analogdata.frames[framename].transpose()
        analog_label = self.analogdata.method_type

        alldata = [cad, cadom, analog]
        keys = [cad_label, cadom_label, analog_label]

        newtable = pd.concat(alldata, keys=keys)
        newtable = newtable.transpose()

        return newtable

    def do_compare_analysis(self, plot_tally_results=False, plot_tally_error=False,
            make_fomtable=False, make_tallytable=False, save_data=False,
            saveformat='txt'):
        '''
        Driver function for the compare solutions.
        '''

        self.saveformat=saveformat

        logger = logging.getLogger("analysis.compare")

        if plot_tally_results == True:
            if self.problem_name:
                newname = self.problem_name.replace(' ','_')
                newname = newname.lower()
                savepath = self.analysis_dir+'/%s_tally_result_compare.pdf' \
                           %newname
            else:
                savepath = self.analysis_dir+'/tally_result_compare.pdf'

            logger.info("plotting tally results at %s" %savepath)
            self.plot_tally_result(savepath=savepath)

        if plot_tally_error == True:
            if self.problem_name:
                newname = self.problem_name.replace(' ','_')
                newname = newname.lower()
                savepath = self.analysis_dir+'/%s_tally_error_compare.pdf' \
                           %newname
            else:
                savepath = self.analysis_dir+'/tally_error_compare.pdf'

            logger.info("plotting tally error at %s" %savepath)
            self.plot_tally_error(savepath=savepath)

        if make_fomtable == True:
            fomtable = self.make_table('fom_frame')

            if self.problem_name:
                newname = self.problem_name.replace(' ','_')
                newname = newname.lower()
                savepath = self.analysis_dir+'/%s_tally_foms_compare' \
                           %newname
            else:
                savepath = self.analysis_dir+'/tally_foms_compare'

            if self.saveformat == 'tex' or self.saveformat == 'latex':
                savepath = savepath+'.tex'
                table = fomtable.to_latex(float_format='%.2f')
            elif self.saveformat == 'txt' or self.saveformat == 'str' or \
            self.saveformat == 'text':
                savepath = savepath+'.txt'
                table = fomtable.to_string(float_format='%.2f')
            else:
                logger.warning('''%s is not a recognized save type. Saving as
                        text instead''' %self.saveformat)
                savepath == savepath+'.txt'
                table = fomtable.to_string(float_format='%.2f')

            logger.info("saving fom table to %s" %savepath)
            with open(savepath, 'w') as fp:
                fp.write(table)

        if make_tallytable == True:
            tallytable = self.make_table('tally_frame')

            if self.problem_name:
                newname = self.problem_name.replace(' ','_')
                newname = newname.lower()
                savepath = self.analysis_dir+'/%s_tally_converge_compare' \
                           %newname
            else:
                savepath = self.analysis_dir+'/tally_converge_compare'

            if self.saveformat == 'tex' or self.saveformat == 'latex':
                savepath = savepath+'.tex'
                table = tallytable.to_latex(float_format='%.2f')
            elif self.saveformat == 'txt' or self.saveformat == 'str' or \
            self.saveformat == 'text':
                savepath = savepath+'.txt'
                table = tallytable.to_string(float_format='%.2f')
            else:
                logger.warning('''%s is not a recognized save type. Saving as
                        text instead''' %self.saveformat)
                savepath == savepath+'.txt'
                table = tallytable.to_string(float_format='%.2f')

            logger.info("saving tally convergence table to %s" %savepath)
            with open(savepath, 'w') as fp:
                fp.write(table)

        if save_data == True:
            datasave = self.analysis_dir+'/compare_data.pkl'

            all_data = {}
            try:
                all_data['tally table']=tallytable
            except NameError:
                all_data['tally table']=self.make_table('tally_frame')

            try:
                all_data['fom table']=fomtable
            except NameError:
                all_data['fom table']=self.make_table('fom_frame')

            logger.info("saving compare data to pickle file")

            with open(datasave, 'w') as fp:
                pickle.dump(all_data, fp)
                fp.close()

###############################################################################
# end of thesiscode/scripts/compare_runs.py
###############################################################################
