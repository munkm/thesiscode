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
from analysis import MCNPOutput, FOMAnalysis, H5Output
from plotting_utils import ( violinbyenergy, stripbyenergy, boxbyenergy,
                           stripbymetric, violinbymetric,
                           boxbymetric, names, energy_histogram )
# from analysis_utils import (get_paths, verify_input_flags, make_logger)
import os
import logging
###############################################################################

def make_logger(name,logfile):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s -- %(name)s : %(message)s')

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    fh = logging.FileHandler(filename=logfile)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def do_single_analysis(base_directory_path, method_type='cadis',
        analysis_directory_name='analysis',
        group_numbers=[], metrics=[], tally_number='44',
        plot_boxes_for_metric=False, plot_boxes_for_energy=False,
        plot_violins_for_metric=False, plot_strip_for_metric=False,
        plot_strip_for_energy=False, plot_violins_for_energy=False,
        plot_FoM_convergence=False,
        plot_RE_by_bin=False, plot_tally_results=False,
        save_FoM_data=False, plot_anisotropy_with_tallydata=False,
        logfile_name='analysis.log'):
    ''' This is the driver script to generate analysis data for a single run.
    The user can choose whether to overwrite previous data, which metrics to
    plot, and where to save that data. By default it will be saved in an
    /analysis/ folder inside the run directory for the hybrid run. '''

    dirpath = os.path.abspath(base_directory_path)
    logfile = '%s/%s' %(dirpath,logfile_name)
    logger = make_logger("analysis", logfile)

    logger.info("acquiring files and directories in directory %s"
            %(base_directory_path))
    filenames, directories = get_paths(base_directory_path,
                                          analysis_directory_name)

    input_flags={'violins_for_metric': plot_violins_for_metric,
            'violins_for_energy': plot_violins_for_energy,
            'boxes_for_metric': plot_boxes_for_metric,
            'boxes_for_energy': plot_boxes_for_energy,
            'strip_for_metric': plot_strip_for_metric,
            'strip_for_energy': plot_strip_for_energy,
            'fom_convergence': plot_FoM_convergence,
            'relative_error_by_bin': plot_RE_by_bin,
            'tally_result' : plot_tally_results,
            'save_fom_data' : save_FoM_data,
            'plot_anisotropy_correlations' : plot_anisotropy_with_tallydata,
            'base_directory' : directories['top_directory'],
            'analysis_data_directory' : directories['analysis_directory']
            }

    logger.info("verifying input flags")
    input_flags = verify_input_flags(input_flags, filenames, directories)

    anisotropy_file = H5Output(filenames['anisotropy_file'])
    analysis_dir = directories['analysis_directory']

    datanames = anisotropy_file.get_datanames()

    if input_flags['violins_for_metric'] == True:
        logger.info("plotting violins for all energies, by  metric")
        metrics = datanames['metric_names']
        for metric in metrics:
            groupdata =  anisotropy_file.get_data_by_metric(metric)
            name = metric_names[metric]
            violinbyenergy(data=groupdata['data'],
                           plot_title='%s Distribution, by Energy group' %(name),
                           x_title='Energy Group No.',
                           y_title='Relative Metric Distribution',
                           savepath=analysis_dir+'/%s_violin.png' %metric,
                           log_scale=True)
        pass

    if input_flags['boxes_for_metric'] == True:
        logger.info("plotting boxes for all energies, by metric")
        metrics = datanames['metric_names']
        for metric in metrics:
            groupdata =  anisotropy_file.get_data_by_metric(metric)
            name = metric_names[metric]
            boxbyenergy(data=groupdata['data'],
                           plot_title='%s Distribution, by Energy group' %(name),
                           x_title='Energy Group No.',
                           y_title='Relative Metric Distribution',
                           savepath=analysis_dir+'/%s_box.png' %metric,
                           log_scale=True)
        pass

    if input_flags['strip_for_metric'] == True:
        logger.info("plotting strips for all energies, by metric")
        metrics = datanames['metric_names']
        for metric in metrics:
            groupdata =  anisotropy_file.get_dataset_by_metric(metric)
            name = metric_names[metric]
            stripbyenergy(data=groupdata['data'],
                           plot_title='%s Distribution, by Energy group' %(name),
                           x_title='Energy Group No.',
                           y_title='Relative Metric Distribution',
                           savepath=analysis_dir+'/%s_strip.png' %metric,
                           log_scale=True)
        pass

    if input_flags['strip_for_energy'] == True:
        logger.info("plotting stripplots for all metrics, monoenergies")
        groups = datanames['energy_groups']
        for group in groups:
            groupdata =  anisotropy_file.get_dataset_by_energy(group)
            name = group_names[group]
            stripbymetric(data=groupdata['data'],
                           plot_title='%s Distribution, by Metric' %(name),
                           x_title='Metric Type',
                           x_names=groupdata['names'],
                           y_title='Relative Metric Distribution Density',
                           savepath=analysis_dir+'/%s_strip.png' %group,
                           log_scale=True)
        pass

    if input_flags['violins_for_energy'] == True:
        logger.info("plotting violinplots for all metrics, monoenergies")
        groups = datanames['energy_groups']
        for group in groups:
            groupdata =  anisotropy_file.get_dataset_by_energy(group)
            name = group_names[group]
            violinbymetric(data=groupdata['data'],
                           plot_title='%s Distribution, by Metric' %(name),
                           x_title='Metric Type',
                           x_names=groupdata['names'],
                           y_title='Relative Metric Distribution',
                           savepath=analysis_dir+'/%s_strip.png' %group,
                           log_scale=True)
        pass

    if input_flags['boxes_for_energy'] == True:
        logger.info("plotting boxplots for each energy group")
        groups = datanames['energy_groups']
        for group in groups:
            groupdata =  anisotropy_file.get_dataset_by_energy(group)
            name = group_names[group]
            boxesbymetric(data=groupdata['data'],
                           plot_title='%s Distribution, by Metric' %(name),
                           x_title='Metric Type',
                           x_names=groupdata['names'],
                           y_title='Box of Metric Distribution',
                           savepath=analysis_dir+'/%s_strip.png' %group,
                           log_scale=True)
        pass

    FOM_init = FOMAnalysis(filenames['mcnp_output_file'], tally_number,
            filenames['timing_file'])

    all_foms = FOM_init.calculate_all_foms()

    MCNP_data = FOM_init.mc_data

    if input_flags['fom_convergence'] == True:
        logger.info("plotting fom convergence for tally %s" %(tallynumber))
        FOM_init.plot_fom_convergence()
        pass

    if input_flags['relative_error_by_bin'] == True:
        logger.info("plotting tally %s relative error at %s" %())
        bins = MCNP_data['tally_data']
        pass

    if input_flags['tally_result'] == True:
        logger.info("plotting tally result at %s ")
        pass

    if input_flags['save_fom_data'] == True:
        logger.info("saving figure of merit data to %s" %filelocation)
        FOM_init.generate_fom_table()
        pass

    anisotropy_stats = anisotropy_file.get_data_statistics()

    if input_flags['plot_anisotropy_correlations'] == True:
        logger.info("plotting anisotropy correlations ")
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

    pass

def verify_input_flags(input_flags, filenames, directories):
    ''' This function will print the value for each of the input flags to a
    log file in the base analysis directory.'''

    logger = logging.getLogger("analysis.input-flags")

    dependencies={'violins_for_metric': ['anisotropy_file'],
            'violins_for_energy': ['anisotropy_file'],
            'boxes_for_metric': ['anisotropy_file'],
            'boxes_for_energy': ['anisotropy_file'],
            'strip_for_metric': ['anisotropy_file'],
            'strip_for_energy': ['anisotropy_file'],
            'fom_convergence': ['mcnp_output_file'],
            'relative_error_by_bin': ['mcnp_output_file'],
            'tally_result' : ['mcnp_output_file'],
            'save_fom_data' : ['mcnp_output_file', 'timing_file'],
            'plot_anisotropy_correlations' : ['mcnp_output_file',
                           'anisotropy_file'],
            }

    input_flags2 = input_flags.copy()

    for flag in input_flags:
        if flag in dependencies and input_flags[flag] == True:
            dependency = dependencies[flag]
            results = dependency[:]
            missing_files = ''
            for i,item in enumerate(dependency):
                if filenames[item] is not None:
                    results[i] = filenames[item]
                else:
                    results[i] = ''
                    missing_files += item + ' '
            if all(results):
                logger.info("all dependencies required to compute %s found" %(flag))
            else:
                logger.warn("flag \"%s\" was set to False by override." %(flag)
                      + " dependency %s was not found" %(missing_files))
                input_flags2[flag]=False
        elif input_flags[flag] == False:
            logger.info('%s will not be computed. Flag set to %s by user.' %(flag,
                input_flags[flag]))
        elif flag not in dependencies:
            logger.info('%s is equal to %s' %(flag, input_flags[flag]))
        else:
            logger.error('%s input flag not found as an expected value' %(flag))

    return(input_flags2)

def check_analysis(path, inputs):
    ''' This function checks for the existence of an analysis directory. It
    will also print a few things to the log file  to make sure the user
    isn't overwriting any valuable direcotries or previously analyzed data. Do
    not choose to set overwrite=True unless you are ok with all of your
    previous data being erased.'''

    return


def get_paths(path, analysis_dirname='analysis'):
    logger = logging.getLogger("analysis.get_paths")
    logger.info("successfully passed logger to get_paths")

    base_dir_path = str(path)
    base_dir_path = os.path.abspath(base_dir_path)

    # check to see where we are in the base_dir
    if os.path.isdir('%s/output' %(base_dir_path)) and \
       os.path.isdir('%s/adj_solution' %(base_dir_path)) or \
       os.path.isdir('%s/fwcadis_adj_solution' %(base_dir_path)):
        logger.info("Base directory found at %s" %(base_dir_path))
    elif os.path.isfile('%s/outp' %base_dir_path) or os.path.isfile('%s/'
            %base_dir_path) or os.path.isfile('%s/' %base_dir_path):
        logger.info("The directory entered is a denovo solution directory." \
                " Moving up one directory")
        base_dir_path = '%s/../' %(base_dir_path)
    else:
        logger.error(" Looked for base directory in %s but the advantg " \
                " file was not found and the weight window file "\
                " in the ouput directory was not found" %(base_dir_path)
                )
        return

    # Now see which adj_directory exists
    if os.path.isdir('%s/adj_solution' %(base_dir_path)):
        adj_dir = '%s/adj_solution' %(base_dir_path)
    elif os.path.isdir('%s/fwcadis_adj_solution' %(base_dir_path)):
        adj_dir = '%s/fwcadis_adj_solution' %(base_dir_path)
    else:
        logger.warn('Can not find adjoint solution directory')
        adj_dir = None
        adj_file_loc = None

    fwd_dir = '%s/fwd_solution' %(base_dir_path)
    if os.path.isdir(fwd_dir):
        logger.info("Found denovo forward solution directory at %s" %(fwd_dir))
    else:
        logger.warn("Forward dir not found at %s" %(fwd_dir))
        fwd_dir = None
        fwd_file_loc = None

    omega_dir = '%s/omega_solution' %(base_dir_path)
    if os.path.isdir(omega_dir):
        logger.info("Found denovo omega solution directory at %s" %(omega_dir))
    else:
        logger.warn("Omega dir not found at %s" %(omega_dir))
        omega_dir = None

    analysis_dir = '%s/%s' %(base_dir_path, analysis_dirname)
    if os.path.isdir(analysis_dir):
        logger.info("Analysis directory and data found at %s" %analysis_dir \
                + " not creating new directory")
    else:
        logger.info("Creating an analysis directory at %s" %(analysis_dir))
        os.makedirs(analysis_dir)

    mcnp_dir = '%s/mcnp' %(base_dir_path)
    if os.path.isdir(mcnp_dir):
        logger.info("Found MCNP solution directory at %s" %(mcnp_dir))
    else:
        logger.warn("MCNP dir not found at %s " %(mcnp_dir))
        mcnp_dir = None

    output_dir = '%s/output' %(base_dir_path)
    if os.path.isdir(output_dir):
        logger.info("Found output solution directory at %s " %(output_dir))
    else:
        logger.warn("Output dir not found at %s " %(output_dir))
        output_dir = None

    timing_file_loc = '%s/timing.json' %(base_dir_path)
    if os.path.isfile(timing_file_loc):
        logger.info("Timing file found at %s " %(timing_file_loc))
    else:
        timing_file_loc = None
        logger.warn("Timing file not found.")

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
