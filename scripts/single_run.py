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
from analysis_utils import (get_paths, verify_input_flags, make_logger,
        metric_names, xscales)
import os
import logging
###############################################################################

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
                                       analysis_dirname=analysis_directory_name)

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
                           savepath=analysis_dir+'/%s_violin.png' %group,
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
                           savepath=analysis_dir+'/%s_boxes.png' %group,
                           log_scale=True)
        pass

    FOM_init = FOMAnalysis(filenames['mcnp_output_file'], tally_number,
            filenames['timing_file'])

    all_foms = FOM_init.calculate_all_foms()

    MCNP_data = FOM_init.mc_data

    if input_flags['fom_convergence'] == True:
        logger.info("plotting fom convergence for tally %s" %(tally_number))
        imagename = 'fom_converge'
        FOM_init.plot_fom_convergence(imagename)
        pass

    if input_flags['relative_error_by_bin'] == True:
        loc = analysis_dir+'/tally_%s_error.png' %(tally_number)
        logger.info("plotting tally %s relative error at %s" %(tally_number,
            loc))
        bins = MCNP_data['tally_data']['energy_groups']
        relative_err = MCNP_data['tally_data']['relative_error']
        energy_histogram(bins, relative_err, loc,
                y_title='tally_relative_error')
        pass

    if input_flags['tally_result'] == True:
        loc = analysis_dir+'/tally_%s_result.png' %(tally_number)
        logger.info("plotting tally %s result at %s" %(tally_number, loc))
        bins = MCNP_data['tally_data']['energy_groups']
        tally_result = MCNP_data['tally_data']['tallied_result']
        energy_histogram(bins, tally_result, loc)
        pass

    if input_flags['save_fom_data'] == True:
        logger.info("saving figure of merit data to %s" %(loc))
        FOM_init.generate_fom_table()
        pass

    if input_flags['save_tally_data'] == True:
        logger.info("saving tally %s convergence data to %s" %(tally_number,loc))

    anisotropy_data = anisotropy_file.get_data_statistics()

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

    if input_flags['save_all_data_json']==True:
        logger.info("saving processed data to %s" %(datasave))
        all_data = {'anisotropy data' : anisotropy_data,
                    'filenames' : filenames,
                    'directories' : directories,
                    'all foms' : all_foms,
                    'mcnp data' : MCNP_data,
                    'input flags' input_flags,
                    'datanames' : datanames,
                    }
        datasave = analysis_dir+'/processed_data.json'

        # dump the processed data to .json file later for accessibility
        with open(datasave, 'w') as fp:
            json.dump(datasave, fp, indent=4)
        pass

    return



###############################################################################
# end of thesiscode/scripts/single-run.py
###############################################################################
