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
from analysis_utils import make_logger
from plotting_utils import energy_histogram, styles
import logging
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

###############################################################################

class Compare_Runs(object):
    def __init__(self, cadisanglefolder='', cadisfolder='', analogfolder='',
            problem_name=''):
        self.cadisangledata = self.get_data(cadisanglefolder, 'cadisangle')
        self.cadisdata = self.get_data(cadisfolder, 'cadis')
        self.analogdata = self.get_data(analogfolder, 'analog')
        self.analysis_dir = self.cadisangledata.directories['analysis_directory']
        self.problem_name = problem_name
        pass

    def get_data(self, folderpath, method_type=''):

        if folderpath:
            data = Single_Run(folderpath, method_type=method_type)
            data.do_single_analysis()
        else:
            data = None

        return data

    def plot_tally_result(self, savepath=None):
        self.plot_compare(compare_type='tallied_result',
                y_label='Tally Result', title='%s comparison of tally result'
                %self.problem_name, savepath=savepath)
        return

    def plot_tally_error(self, savepath=None):
        self.plot_compare(compare_type='relative_error',
                y_label='Tally Relative Error',
                title='%s comparison of tally relative error'
                %self.problem_name, savepath=savepath)
        return

    def plot_compare(self, compare_type='tallied_result',
                     savepath=None, y_label='', title=''):
        energy_groups = \
            self.cadisangledata.MCNP_data['tally_data']['energy_groups']
        cadang = self.cadisangledata.MCNP_data['tally_data'][compare_type]
        cad = self.cadisdata.MCNP_data['tally_data'][compare_type]*1.05
        analog = self.analogdata.MCNP_data['tally_data'][compare_type]*1.10

        fig = plt.figure()

        energy_histogram(energy_groups, cadang, None,
                **styles[self.cadisangledata.method_type])
        energy_histogram(energy_groups, cad, None,
                **styles[self.cadisdata.method_type])
        energy_histogram(energy_groups, analog, None,
                **styles[self.analogdata.method_type])

        # plt.legend(loc=best)
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
        print('composite frame of %s being created' %framename)

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
            make_fomtable=False, make_tallytable=False):

        if plot_tally_results == True:
            if self.problem_name:
                savepath = self.analysis_dir+'/%s_tally_result_compare.png' \
                           %self.problem_name
            else:
                savepath = self.analysis_dir+'/tally_result_compare.png'

            self.plot_tally_result(savepath=savepath)

        if plot_tally_error == True:
            if self.problem_name:
                savepath = self.analysis_dir+'/%s_tally_error_compare.png' \
                           %self.problem_name
            else:
                savepath = self.analysis_dir+'/tally_error_compare.png'

            self.plot_tally_error(savepath=savepath)

        if make_fomtable == True:
            table = self.make_table('fom_frame')

            if self.problem_name:
                savepath = self.analysis_dir+'/%s_tally_foms_compare.txt' \
                           %self.problem_name
            else:
                savepath = self.analysis_dir+'/tally_foms_compare.txt'

            table = table.to_string(float_format='%.2f')
            with open(savepath, 'w') as fp:
                fp.write(table)

        if make_tallytable == True:
            table = self.make_table('tally_frame')

            if self.problem_name:
                savepath = self.analysis_dir+'/%s_tally_converge_compare.txt' \
                           %self.problem_name
            else:
                savepath = self.analysis_dir+'/tally_converge_compare.txt'

            table = table.to_string()
            with open(savepath, 'w') as fp:
                fp.write(table)

###############################################################################
# end of thesiscode/scripts/compare_runs.py
###############################################################################
