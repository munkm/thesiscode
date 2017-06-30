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
                           boxbymetric, names, energy_histogram, styles )
from analysis_utils import (get_paths, verify_input_flags, format_logger,
        metric_names, group_names, xscales, get_method_type, selection_names)
import json
import pickle
import os
import logging
###############################################################################

class Single_Run(object):

    def __init__(self, base_directory_path, method_type='',
        logfile_name='analysis.log'):

        if method_type:
            method_name=method_type
        else:
            method_name='unknown method'

        # initialize logger
        base_directory_path = os.path.expanduser(base_directory_path)
        dirpath = base_directory_path

        # dirpath = os.path.abspath(base_directory_path)
        logger = logging.getLogger("analysis")

        if logger.handlers:
            logger = logger
        else:
            logfile = '%s/%s' %(dirpath,logfile_name)
            logger = format_logger("analysis", logfile)

        logger.info("initialized %s analysis %s " %(method_type,__name__))

        # set variables for later
        self.base_directory_path = base_directory_path
        self.method_type = method_type
        self.directories = None
        self.filenames = None
        self.input_flags = None
        self.datanames = None

        # set dataobjects
        self.foms = None
        self.MCNP_data = None
        self.anisotropy_data = None

        pass

    def do_single_analysis(self, analysis_directory_name='analysis',
            group_numbers=[], metrics=[], tally_number='44',
            plot_boxes_for_metric=False, plot_boxes_for_energy=False,
            plot_violins_for_metric=False, plot_strip_for_metric=False,
            plot_strip_for_energy=False, plot_violins_for_energy=False,
            plot_FoM_convergence=False,
            plot_RE_by_bin=False, plot_tally_results=False,
            save_FoM_data=False, save_tally_data=False,
            plot_anisotropy_with_tallydata=False,
            plot_anisotropies_median=False, plot_anisotropies_mean=False,
            save_data_json=False, select_anisotropies='full'):
        ''' This is the driver script to generate analysis data for a single run.
        The user can choose whether to overwrite previous data, which metrics to
        plot, and where to save that data. By default it will be saved in an
        /analysis/ folder inside the run directory for the hybrid run. '''

        logger=logging.getLogger("analysis.single_run")
        logger.info("acquiring files and directories in directory %s"
                %(self.base_directory_path))
        filenames, directories = get_paths(self.base_directory_path,
                                analysis_dirname=analysis_directory_name)

        self.filenames = filenames
        self.directories = directories

        method_type = get_method_type(filenames, directories)

        if self.method_type:
            if self.method_type != method_type:
                logger.warning("User-defined method type and detected method" \
                        + "type do not match. \n User defined: %s"%self.method_type\
                        + "\n Detected: %s" %method_type \
                        + "\n Using user-specified method.")
            elif self.method_type == method_type:
                logger.info("User-defined method type and detected type match" \
                        + " as: %s" %self.method_type)
        else:
            logger.info("No method type specified by user. \n Using detected" \
                    + " type: %s" %method_type)
            self.method_type = method_type

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
                'save_tally_data' : save_tally_data,
                'save_all_data' : save_data_json,
                'plot_anisotropy_correlations' : plot_anisotropy_with_tallydata,
                'plot_anisotropy_corrs_median' :plot_anisotropies_median,
                'plot_anisotropy_corrs_mean' : plot_anisotropies_mean,
                'select_anisotropies' : select_anisotropies,
                'base_directory' : directories['top_directory'],
                'analysis_data_directory' : directories['analysis_directory']
                }

        logger.info("verifying input flags")
        input_flags = verify_input_flags(input_flags, filenames, directories)
        self.input_flags = input_flags

        if input_flags['strip_for_metric'] == True or \
        input_flags['violins_for_metric'] == True or \
        input_flags['boxes_for_metric'] == True or \
        input_flags['strip_for_energy'] == True or \
        input_flags['violins_for_energy'] == True or \
        input_flags['boxes_for_energy'] == True or \
        input_flags['plot_anisotropy_correlations'] == True or \
        input_flags['plot_anisotropy_corrs_median'] == True or \
        input_flags['plot_anisotropy_corrs_mean'] == True:
            anisotropy_file = H5Output(filenames['anisotropy_file'])
            datanames = anisotropy_file.get_datanames()
            self.datanames=datanames

        analysis_dir = directories['analysis_directory']

        if input_flags['strip_for_metric'] == True or \
        input_flags['violins_for_metric'] == True or \
        input_flags['boxes_for_metric'] == True:
            logger.info("Starting plotting routines for single metric, all"
                    + " energy groups")

            metrics = datanames['metric_names']
            if 'contributon_flux' in metrics:
                metrics.remove('contributon_flux')
            for metric in metrics:
                groupdata =  anisotropy_file.get_data_by_metric(metric,
                        cutoff=input_flags['select_anisotropies'])
                subdata = anisotropy_file.get_dataset_by_metric(metric,
                        num_samples = 1500,
                        cutoff=input_flags['select_anisotropies'])

                # get the data for labelling the plot
                if metric in metric_names:
                    name = metric_names[metric]
                else:
                    name = metric
                select = input_flags['select_anisotropies']
                if select in selection_names:
                    selection = selection_names[select]
                else:
                    selection = select
                full_title = '%s Distribution, by Energy Group, %s' %(name,
                        selection)

                if input_flags['violins_for_metric'] == True:
                    logger.info("plotting violins for all energies, %s" %(name))
                    violinbyenergy(data=groupdata['data'],
                                   plot_title=full_title,
                                   x_title='Energy Group No.',
                                   y_title='Relative Metric Distribution',
                                   savepath=analysis_dir+'/%s_violin_%s.pdf'
                                             %(metric, select),
                                   log_scale=True)

                if input_flags['boxes_for_metric'] == True:
                    logger.info("plotting boxes for all energies, %s" %(name))
                    boxbyenergy(data=groupdata['data'],
                                   plot_title=full_title,
                                   x_title='Energy Group No.',
                                   y_title='Relative Metric Distribution',
                                   savepath=analysis_dir+'/%s_box_%s.pdf'
                                             %(metric, select),
                                   log_scale=True)

                if input_flags['strip_for_metric'] == True:
                    logger.info("plotting strips for all energies, %s" %(name))
                    stripbyenergy(data=subdata['data'],
                                   plot_title=full_title,
                                   x_title='Energy Group No.',
                                   y_title='Relative Metric Distribution',
                                   savepath=analysis_dir+'/%s_strip_%s.pdf'
                                             %(metric, select),
                                   log_scale=True)


        if input_flags['strip_for_energy'] == True or \
        input_flags['violins_for_energy'] == True or \
        input_flags['boxes_for_energy'] == True:
            logger.info("Starting plotting routines for monoenergic plots, all"
                    + " metric types")
            groups = datanames['energy_groups']
            for group in groups:
                groupdata =  anisotropy_file.get_data_by_energy(group,
                        cutoff=input_flags['select_anisotropies'])
                subdata = anisotropy_file.get_dataset_by_energy(group,
                        num_samples = 1500,
                        cutoff=input_flags['select_anisotropies'])

                # get the information to label the plots
                if group in group_names:
                    name = group_names[group]
                else:
                    name = group
                select = input_flags['select_anisotropies']
                if select in selection_names:
                    selection = selection_names[select]
                else:
                    selection = select
                full_title = '%s Distribution, by Metric, %s' %(name,
                        selection)

                if input_flags['strip_for_energy'] == True:
                    logger.info("plotting stripplots for all metrics, %s"
                            %(name))
                    stripbymetric(data=subdata['data'],
                                   plot_title=full_title,
                                   x_title='Metric Type',
                                   x_names=groupdata['names'],
                                   y_title='Relative Metric Distribution Density',
                                   savepath=analysis_dir+'/%s_strip_%s.pdf'
                                             %(group, select),
                                   log_scale=True)

                if input_flags['violins_for_energy'] == True:
                    logger.info("plotting violinplots for all metrics, %s"
                            %(group))
                    violinbymetric(data=groupdata['data'],
                                   plot_title=full_title,
                                   x_title='Metric Type',
                                   x_names=groupdata['names'],
                                   y_title='Relative Metric Distribution',
                                   savepath=analysis_dir+'/%s_violin_%s.pdf'
                                             %(group, select),
                                   log_scale=True)

                if input_flags['boxes_for_energy'] == True:
                    logger.info("plotting boxplots for all metrics, %s" %(name))
                    boxbymetric(data=groupdata['data'],
                                   plot_title=full_title,
                                   x_title='Metric Type',
                                   x_names=groupdata['names'],
                                   y_title='Box of Metric Distribution',
                                   savepath=analysis_dir+'/%s_boxes_%s.pdf'
                                             %(group, select),
                                   log_scale=True)

        if filenames['mcnp_output_file'] is not None:
            if filenames['timing_file'] is not None:
                logger.debug("Calculating FOMs for Monte Carlo and adjusted"
                        + " deterministic runtimes." )
                FOM_init = FOMAnalysis(filenames['mcnp_output_file'], tally_number,
                        deterministic_timing_file=filenames['timing_file'],
                        omnibus_output_file=filenames['omni_out_file'])
            else:
                logger.debug("No timing file found. Calculating FOMs for"
                        + " standard Monte Carlo without deterministic "
                        + "timing adjustments")
                FOM_init = FOMAnalysis(filenames['mcnp_output_file'],
                        tally_number)

            all_foms = FOM_init.calculate_all_foms()
            MCNP_data = FOM_init.mc_data

            self.foms = all_foms
            self.MCNP_data = MCNP_data
            self.frames = {'fom_frame': FOM_init.fom_frame,
                           'tally_frame': FOM_init.tally_frame,
                           'timing_frame': FOM_init.timing_frame}
        else:
            logger.warning("The MCNP output file was not found. Checked in"
                    + " %s. None of the analyses " %directories['mcnp_directory']
                    + "relevant to the Monte Carlo analysis can be performed.")


        if input_flags['fom_convergence'] == True:
            logger.info("plotting fom convergence for tally %s" %(tally_number))
            imagename = 'fom_converge'
            FOM_init.plot_fom_convergence(imagename)

        if input_flags['relative_error_by_bin'] == True:
            loc = analysis_dir+'/tally_%s_error.pdf' %(tally_number)
            logger.info("plotting tally %s relative error at %s" %(tally_number,
                loc))
            bins = MCNP_data['tally_data']['energy_groups']
            relative_err = MCNP_data['tally_data']['relative_error']
            energy_histogram(bins, relative_err, loc,
                    y_title='Tally Relative Error', **styles[self.method_type])

        if input_flags['tally_result'] == True:
            loc = analysis_dir+'/tally_%s_result.pdf' %(tally_number)
            logger.info("plotting tally %s result at %s" %(tally_number, loc))
            bins = MCNP_data['tally_data']['energy_groups']
            tally_result = MCNP_data['tally_data']['tallied_result']
            energy_histogram(bins, tally_result, loc, **styles[self.method_type])

        if input_flags['save_fom_data'] == True:
            loc = analysis_dir+'/tally_%s_foms.txt' %(tally_number)
            logger.info("saving figure of merit data to %s" %(loc))
            foms = FOM_init.print_tally_foms(printtype='str', float_format='%.2f')
            with open(loc, 'w') as fp:
                fp.write(foms)
                fp.close()

        if input_flags['save_tally_data'] == True:
            loc = analysis_dir+'/tally_%s_converg.txt' %(tally_number)
            logger.info("saving tally %s convergence data to %s" %(tally_number,loc))
            conv = FOM_init.print_tally_convergence(printtype='str')
            with open(loc, 'w') as fp:
                fp.write(conv)

        self.anisotropy_data = {}

        if input_flags['plot_anisotropy_correlations'] == True or \
           input_flags['plot_anisotropy_corrs_median'] == True or \
           input_flags['plot_anisotropy_corrs_mean'] == True:
            # first calculate anisotropy stats

            from plotting_utils import statscatter
            err = MCNP_data['tally_data']['relative_error']
            bins = MCNP_data['tally_data']['energy_groups']

            # because in the deterministic calculation, the first group is the
            # highest energy, check that MC data is in the same order.
            if bins[-1] > bins[0]:
                logger.debug('''tally bins not in the same order as
                        deterministic result. Reversing order for consistency.''')
                err = err[::-1]
                bins = bins[::-1]
            else:
                logger.debug('''Monte Carlo and deterministic results in same
                        energy order.''')


            if input_flags['plot_anisotropy_correlations'] == True:
                logger.info("calculating anisotropy statistics for metrics")
                anisotropy_data = anisotropy_file.get_data_statistics()
                self.anisotropy_data['full']=anisotropy_data

                # plot the anisotropy stats
                logger.info("plotting anisotropy correlations ")
                data = anisotropy_data['data']
                for metric in anisotropy_data['metrics']:
                    loc = analysis_dir+'/%s_stats.pdf' %(metric)
                    name = metric_names[metric]
                    scale = xscales[metric]
                    metric_location = anisotropy_data['metrics'].index(metric)
                    metric_data = anisotropy_data['data'][metric_location]
                    x1 = metric_data[:,0]
                    x2 = metric_data[:,1]
                    x4 = metric_data[:,3]
                    statscatter(x1,x2,x4, err, savepath=loc, metric_name=name,
                            scale=scale)

            if input_flags['plot_anisotropy_corrs_median'] == True:
                logger.info("calculating anisotropy statistics for metrics")
                anisotropy_data = anisotropy_file.get_data_statistics(
                        filter_data=True, cutoff='median')
                self.anisotropy_data['median']=anisotropy_data

                # plot the anisotropy stats
                logger.info("plotting anisotropy correlations for anisotropy"
                           + " values above the median value")
                data = anisotropy_data['data']
                for metric in anisotropy_data['metrics']:
                    loc = analysis_dir+'/%s_stats_median.pdf' %(metric)
                    name = metric_names[metric]
                    scale = xscales[metric]
                    metric_location = anisotropy_data['metrics'].index(metric)
                    metric_data = anisotropy_data['data'][metric_location]
                    x1 = metric_data[:,0]
                    x2 = metric_data[:,1]
                    x4 = metric_data[:,3]
                    statscatter(x1,x2,x4, err, savepath=loc, metric_name=name,
                            scale=scale)

            if input_flags['plot_anisotropy_corrs_mean'] == True:
                logger.info("calculating anisotropy statistics for metrics")
                anisotropy_data = anisotropy_file.get_data_statistics(
                        filter_data=True, cutoff='mean')
                self.anisotropy_data['mean']=anisotropy_data

                # plot the anisotropy stats
                logger.info("plotting anisotropy correlations for anisotropy"
                           + " values above the mean value")
                data = anisotropy_data['data']
                for metric in anisotropy_data['metrics']:
                    loc = analysis_dir+'/%s_stats_mean.pdf' %(metric)
                    name = metric_names[metric]
                    scale = xscales[metric]
                    metric_location = anisotropy_data['metrics'].index(metric)
                    metric_data = anisotropy_data['data'][metric_location]
                    x1 = metric_data[:,0]
                    x2 = metric_data[:,1]
                    x4 = metric_data[:,3]
                    statscatter(x1,x2,x4, err, savepath=loc, metric_name=name,
                            scale=scale)

        if input_flags['save_all_data']==True:
            varsave = analysis_dir+'/processed_data.json'
            datasave = analysis_dir+'/processed_data.pkl'

            logger.info("saving processed data to %s" %(datasave))
            all_data = {
                        'all foms' : self.foms,
                        'mcnp data' : self.MCNP_data,
                        'anisotropy data' : self.anisotropy_data,
                        }

            # dump the processed data to .pickle file later for accessibility
            with open(datasave, 'w') as fp:
                pickle.dump(all_data, fp)
                fp.close()

            logger.info("saving processed variables to %s" %(varsave))
            all_vars = {
                        'filenames' : self.filenames,
                        'directories' : self.directories,
                        'input flags': self.input_flags,
                        'datanames' : self.datanames,
                        }

            with open(varsave, 'w') as fp:
                json.dump(all_vars, fp, indent=4)
                fp.close()

        return

###############################################################################
# end of thesiscode/scripts/single-run.py
###############################################################################
