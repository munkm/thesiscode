###############################################################################
# File  : thesiscode/scripts/single-run.py
# Author: madicken
# Date  : Tue Mar 21 15:49:14 2017
#
# <+Description+>
###############################################################################
from __future__ import (division, absolute_import, print_function, )
#-----------------------------------------------------------------------------#
import numpy as np
from mcnpoutput import TrackLengthTally
from plotting_utils import ( violinbyenergy, stripbygroup, violinbygroup, names,
                          energy_histogram )
###############################################################################

def do_analysis(base_directory_path, analysis_directory_name='analysis',
        group_numbers=[], metrics=[], tally_number='44',
        plot_violins_by_group=False, plot_strip_by_group=False,
        plot_violins_by_energy=False, plot_FoM_convergence=False,
        plot_RE_by_bin=False, plot_tally_results=False,
        save_FoM_data=False):

    inputs={'violins_by_group': violins_by_group,
            'violins_by_energy': violins_by_energy,
            '':}

    verify_input_flags(inputs):

    if plot_violins_by_group == True:
        pass

    if plot_strip_by_group == True:
        pass

    if plot_violins_by_energy == True:
        pass

    if plot_FoM_convergence == True:
        pass

    if plot_RE_by_bin == True:
        pass

    if plot_tally_results == True:
        pass

    if save_FoM_data == True:
        pass


def verify_input_flags(inputs):
    ''' This function will print the value for each of the input flags to a
    textfile in the base analysis directory.'''
    return variables

def check_analysis(path, inputs):
    ''' This function checks for the existence of an analysis directory. It
    will also print a few things to the command line to make sure the user
    isn't overwriting any valuable direcotries or previously analyzed data'''

#-----------------------------------------------------------------------------#

###############################################################################
# end of thesiscode/scripts/single-run.py
###############################################################################
