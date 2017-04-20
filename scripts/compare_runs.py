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

    def plot_tally_result(self):
        self.plot_compare(compare_type='tallied_result',
                y_label='Tally Result', title='%s comparison of tally result'
                %self.problem_name)
        return

    def plot_tally_error(self):
        self.plot_compare(compare_type='relative_error',
                y_label='Tally Relative Error',
                title='%s comparison of tally relative error' %self.problem_name)
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

    def make_fom_table(self):
        cad = self.cadisdata.frames['fom_frame'].transpose()
        cadom = self.cadisangledata.frames['fom_frame'].transpose()
        analog = self.cadisangledata.frames['fom_frame'].transpose()

        alldata = [cad, cadom, analog]
        keys = [cad_label, cadom_label, analog_label]

        newtable = pd.concat(alldata, keys=keys)
        newtable = newtable.transpose()

        return newtable

    def make_tallytable(self):

        return

    def do_compare_analysis(self, plot_tally_results=False, plot_tally_error=False,
            make_fom_table=False):

        if plot_tally_results == True:
            if problem_name:
                savepath = self.analysis_dir+'/%s_tally_result_compare.png' %problem_name
            else:
                savepath = self.analysis_dir+'/tally_result_compare.png'

            self.plot_tally_result(savepath=savepath)

        if plot_tally_error == True:
            self.plot_tally_error()

        if make_fom_table == True:
            self.make_fom_table()

        if make_tallytable == True:
            self.make_tally_table()

###############################################################################
# end of thesiscode/scripts/compare_runs.py
###############################################################################
