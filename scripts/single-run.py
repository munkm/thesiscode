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
from analysis import MCNPOutput
from plotting_utils import ( violinbyenergy, stripbygroup, violinbygroup, names,
                          energy_histogram )
###############################################################################

def do_single_analysis(base_directory_path, analysis_directory_name='analysis',
        group_numbers=[], metrics=[], tally_number='44',
        plot_violins_by_group=False, plot_strip_by_group=False,
        plot_violins_by_energy=False, plot_FoM_convergence=False,
        plot_RE_by_bin=False, plot_tally_results=False,
        save_FoM_data=False, logfile_name='logger.log'):
    ''' This is the driver script to generate analysis data for a single run.
    The user can choose whether to overwrite previous data, which metrics to
    plot, and where to save that data. By default it will be saved in an
    /analysis/ folder inside the run directory for the hybrid run. '''

    filnames, directories = get_filenames(base_directory_path)

    input_flags={'violins_by_group': plot_violins_by_group,
            'violins_by_energy': plot_violins_by_energy,
            'strip_by_group':plot_strip_by_group,
            'FoM convergence': plot_FoM_convergence,
            'Relative Error by bin': plot_RE_by_bin,
            'Tally Result' : plot_tally_results,
            'save FoM data' : save FoM data,
            'base directory' : base_directory_path,
            'analysis data directory' : full_analysis_dir
            }

    verify_input_flags(input_flags):

    if plot_violins_by_group == True:
        for
        pass

    if plot_strip_by_group == True:
        pass

    if plot_violins_by_energy == True:
        pass

    MCNP_data = MCNPOutput(filennames['mcnp_output'],
            tallynumber=tallynumber).get_tally_data()

    if plot_FoM_convergence == True:
        pass

    if plot_RE_by_bin == True:
        bins = MCNP_data['tally_data'][]
        pass

    if plot_tally_results == True:
        pass

    if save_FoM_data == True:
        pass


def verify_input_flags(inputs, filename=variables.log):
    ''' This function will print the value for each of the input flags to a
    textfile in the base analysis directory.'''

    return variables

def check_analysis(path, inputs):
    ''' This function checks for the existence of an analysis directory. It
    will also print a few things to the command line to make sure the user
    isn't overwriting any valuable direcotries or previously analyzed data. Do
    not choose to set overwrite=True unless you are ok with all of your
    previous data being erased.'''

    return


def get_paths(path):
    base_dir_path = os.path.abspath(base_dir_path)
    # check to see where we are in the base_dir
    if os.path.isdir()

    filenames = {'timing_file' : timing_file_loc,
                 'anisotropy_file' : anisotropy_file_loc,
                 'mcnp_output_file' : mcnp_output_loc,
                 'wwinp_file': wwinp_loc,
                 'meshtal_file' : mesh_results_loc,
                 }

    directories = {'mcnp_directory' : mcnp_dir,
                   'top_directory' : base_dir_path,
                   'forward_directory' : fwd_dir,
                   'adjoint_directory' : adj_dir,
                   'analysis_directory' : analysis_dir
                   }

    return(filenames, directories)


#-----------------------------------------------------------------------------#

###############################################################################
# end of thesiscode/scripts/single-run.py
###############################################################################
