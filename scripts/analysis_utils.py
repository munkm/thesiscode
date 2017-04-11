###############################################################################
# File  : thesiscode/scripts/analysis_utils.py
# Author: madicken
# Date  : Tue April 11 10:14:14 2017
#
# <+Description+>
###############################################################################
from __future__ import (division, absolute_import, print_function, )
#-----------------------------------------------------------------------------#
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
# end of thesiscode/scripts/analysis_utils.py
###############################################################################
