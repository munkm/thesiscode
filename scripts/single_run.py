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
import os
###############################################################################


def do_single_analysis(base_directory_path, analysis_directory_name='analysis',
        group_numbers=[], metrics=[], tally_number='44',
        plot_violins_by_group=False, plot_strip_by_group=False,
        plot_violins_by_energy=False, plot_FoM_convergence=False,
        plot_RE_by_bin=True, plot_tally_results=True,
        save_FoM_data=False, plot_anisotropy_with_tallydata=False,
        logfile_name='logger.log'):
    ''' This is the driver script to generate analysis data for a single run.
    The user can choose whether to overwrite previous data, which metrics to
    plot, and where to save that data. By default it will be saved in an
    /analysis/ folder inside the run directory for the hybrid run. '''

    filnames, directories = get_paths(base_directory_path,
                                          analysis_directory_name)

    input_flags={'violins_by_group': plot_violins_by_group,
            'violins_by_energy': plot_violins_by_energy,
            'strip_by_group':plot_strip_by_group,
            'FoM convergence': plot_FoM_convergence,
            'Relative Error by bin': plot_RE_by_bin,
            'Tally Result' : plot_tally_results,
            'save FoM data' : save_FoM_data,
            'Plot anisotropy correlations' : plot_anisotropy_with_tallydata,
            'base directory' : base_directory_path,
            'analysis data directory' : full_analysis_dir
            }

    verify_input_flags(input_flags)

    datanames = H5Ouput(filenames['anisotropy_file']).get_datanames()

    if plot_violins_by_group == True:
        metrics = datanames['metric_names']
        for metric in metrics:
            groupdata =  \
                   H5output(filenames['anisotropy_file']).get_data_by_group(metric)
            name = metric_names[metric]
            violinbyenergy(data=groupdata['data'],
                           plot_title='%s Distribution, by Energy group' %(name),
                           x_title='Energy Group No.',
                           y_title='Relative Metric Distribution',
                           savepath=dirs['analysis_directory']+'/%s_violin.png' %metric)
        pass

    if plot_strip_by_group == True:
        metrics = datanames['metric_names']
        for metric in metrics:
            groupdata =  \
                   H5output(filenames['anisotropy_file']).get_data_by_group(metric)
            newdata = np.random.choice(groupdata['data']
            name = metric_names[metric]
            stripbyenergy(data=groupdata['data'],
                           plot_title='%s Distribution, by Energy group' %(name),
                           x_title='Energy Group No.',
                           y_title='Relative Metric Distribution',
                           savepath=dirs['analysis_directory']+'/%s_strip.png' %metric)
        pass

    if plot_violins_by_energy == True:
        pass

    MCNP_data = MCNPOutput(filennames['mcnp_output'],
            tallynumber=tallynumber).get_tally_data()

    if plot_FoM_convergence == True:
        pass

    if plot_RE_by_bin == True:
        bins = MCNP_data['tally_data']
        pass

    if plot_tally_results == True:
        pass

    if save_FoM_data == True:
        pass

    anisotropy_stats = H5Output(filenames['']).get_data_statistics()

    if plot_anisotropy_with_tallydata == True:
        from plotting_utils import statscatter
        err = MCNP_data['tally_data']['relative_error']
        data = anisotropy_data['data']
        for metric in anisotropy_data['metrics']:
            name = metric_names[metric]
            scale = xscales[metric]
            metric_location = anisotropy_data['metrics'].index(metric)
            metric_data = anisotropy_data[metric_location]
            x1 = metric_data[:,0]
            x2 = metric_data[:,1]
            x4 = metric_data[:,3]
            statscatter(x1,x2,x4, err, savepath='' %(metric), metric_name=name,
                    scale=scale)
        pass


def verify_input_flags(inputs, filename='variables.log'):
    ''' This function will print the value for each of the input flags to a
    textfile in the base analysis directory.'''

    variables = None

    return variables

def check_analysis(path, inputs):
    ''' This function checks for the existence of an analysis directory. It
    will also print a few things to the command line to make sure the user
    isn't overwriting any valuable direcotries or previously analyzed data. Do
    not choose to set overwrite=True unless you are ok with all of your
    previous data being erased.'''

    return


def get_paths(path, analysis_dirname='analysis'):
    base_dir_path = str(path)
    base_dir_path = os.path.abspath(base_dir_path)

    # check to see where we are in the base_dir
    if os.path.isdir('%s/output' %(base_dir_path)) and \
       os.path.isdir('%s/adj_solution' %(base_dir_path)) or \
       os.path.isdir('%s/fwcadis_adj_solution' %(base_dir_path)):
        print("Base directory found at %s \n" %(base_dir_path))
    elif os.path.isfile('%s/outp' %base_dir_path) or os.path.isfile('%s/'
            %base_dir_path) or os.path.isfile('%s/' %base_dir_path):
        print("The directory entered is a denovo solution directory." \
                " Moving up one directory \n")
        base_dir_path = '%s/../' %(base_dir_path)
    else:
        print(" Looked for base directory in %s but the advantg " \
                " file was not found and the weight window file "\
                " in the ouput directory was not found \n" %(base_dir_path)
                )
        return

    # Now see which adj_directory exists
    if os.path.isdir('%s/adj_solution' %(base_dir_path)):
        adj_dir = '%s/adj_solution' %(base_dir_path)
    elif os.path.isdir('%s/fwcadis_adj_solution' %(base_dir_path)):
        adj_dir = '%s/fwcadis_adj_solution' %(base_dir_path)
    else:
        print('Can not find adjoint solution directory \n')
        adj_dir = None
        adj_file_loc = None

    fwd_dir = '%s/fwd_solution' %(base_dir_path)
    if os.path.isdir(fwd_dir):
        print("Found denovo forward solution directory at %s \n" %(fwd_dir))
    else:
        print("Forward dir not found at %s \n" %(fwd_dir))
        fwd_dir = None
        fwd_file_loc = None

    omega_dir = '%s/omega_solution' %(base_dir_path)
    if os.path.isdir(omega_dir):
        print("Found denovo omega solution directory at %s \n" %(omega_dir))
    else:
        print("Omega dir not found at %s \n" %(omega_dir))
        omega_dir = None

    analysis_dir = '%s/%s' %(base_dir_path, analysis_dirname)
    if os.path.isdir(analysis_dir):
        print("Analysis directory and data found at %s, not creating \
                new directory \n" %(analysis_dir))
    else:
        print("Creating an analysis directory at %s \n" %(analysis_dir))
        os.makedirs(analysis_dir)

    mcnp_dir = '%s/mcnp' %(base_dir_path)
    if os.path.isdir(mcnp_dir):
        print("Found MCNP solution directory at %s \n" %(mcnp_dir))
    else:
        print("MCNP dir not found at %s \n" %(mcnp_dir))
        mcnp_dir = None

    output_dir = '%s/output' %(base_dir_path)
    if os.path.isdir(output_dir):
        print("Found output solution directory at %s \n" %(output_dir))
    else:
        print("Output dir not found at %s \n" %(output_dir))
        output_dir = None

    timing_file_loc = '%s/timing.json' %(base_dir_path)
    if os.path.isfile(timing_file_loc):
        print("Timing file found at %s \n" %(timing_file_loc))
    else:
        timing_file_loc = None

    anisotropy_file_loc = '%s/problem_anisotropies.h5' %(omega_dir)
    omega_file_loc = '%s/denovo_omega_output.silo' %(omega_dir)
    if omega_dir is not None:
        if os.path.isfile(anisotropy_file_loc):
            pass
        else:
            anisotropy_file_loc = None
        if os.path.isfile(omega_file_loc):
            pass
        else:
            omega_file_loc = None
    else:
        ansiotropy_file_loc, omega_file_loc = None, None

    fwd_file_loc = '%s/denovo_forward_output.silo' %(fwd_dir)
    if fwd_dir is not None and os.path.isfile(fwd_file_loc):
        fwd_file_loc = fwd_file_loc
    else:
        fwd_file_loc = None

    adj_file_loc = '%s/denovo_adjoint_output.silo' %(adj_dir)
    if adj_dir is not None and os.path.isfile(adj_file_loc):
        adj_file_loc = adj_file_loc
    else:
        adj_file_loc = None

    output_file_loc = '%s/fields.silo' %(output_dir)
    if output_dir is not None and os.path.isfile(output_file_loc):
        output_file_loc = output_file_loc
    else:
        output_file_loc = None

    if mcnp_dir is not None:
        mcnp_output_loc = '%s/out' %(mcnp_dir)
        wwinp_loc = '%s/wwinp' %(mcnp_dir)
        mesh_results_loc = '%s/meshtal' %(mcnp_dir)
    else:
        mcnp_output_loc, wwinp_loc, mesh_results_loc = None, None, None


    filenames = {'timing_file' : timing_file_loc,
                 'anisotropy_file' : anisotropy_file_loc,
                 'omega_flux_file': omega_file_loc,
                 'fwd_flux_file' : fwd_file_loc,
                 'adj_flux_file' : adj_file_loc,
                 'output_file' : output_file_loc,
                 'mcnp_output_file' : mcnp_output_loc,
                 'wwinp_file': wwinp_loc,
                 'meshtal_file' : mesh_results_loc,
                 }

    directories = {'mcnp_directory' : mcnp_dir,
                   'top_directory' : base_dir_path,
                   'forward_directory' : fwd_dir,
                   'adjoint_directory' : adj_dir,
                   'omega_directory' : omega_dir,
                   'analysis_directory' : analysis_dir,
                   'output_directory' : output_dir,
                   }

    return(filenames, directories)


#-----------------------------------------------------------------------------#

# A few useful dicts that can be used for convenience. metric_names is used for
# formatting so in plot titles (and whatnot) a simple lookup can be performed
# and an appropriately formatted title will be returned.
#

metric_names = {u'adjoint_anisotropy': 'Adjoint Anisotropy',
         u'forward_anisotropy': 'Forward Anisotropy',
         u'metric_five': 'Metric Five',
         u'metric_four': 'Metric Four',
         u'metric_one': 'Metric One',
         u'metric_six': 'Metric Six',
         u'metric_three': 'Metric Three',
         u'metric_two': 'Metric Two'}

xscales = {u'adjoint_anisotropy': 'linear',
         u'forward_anisotropy': 'linear',
         u'metric_five': 'log',
         u'metric_four': 'linear',
         u'metric_one': 'log',
         u'metric_six': 'log',
         u'metric_three': 'linear',
         u'metric_two': 'linear'}

# color_dists = {'purples': sns.cubehelix_palette(12),
#               'groupwise': sns.diverging_palette(10, 240, n=27)}
###############################################################################
# end of thesiscode/scripts/single-run.py
###############################################################################
