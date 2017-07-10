###############################################################################
# File  : thesiscode/scripts/plotting_utils.py
# Author: madicken
# Date  : Wed Mar 15 13:43:12 2017
#
# This script contains a few different plotting utilities that are used
# frequently in the analysis of the data from my dissertation.
#
###############################################################################
from __future__ import (division, absolute_import, print_function, )
#-----------------------------------------------------------------------------#
import numpy as np
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import gridspec
import logging
###############################################################################

# Default Values for various things

names = [u'adjoint_anisotropy', u'forward_anisotropy', u'metric_five',
u'metric_four', u'metric_one', u'metric_six', u'metric_three', u'metric_two']


#-----------------------------------------------------------------------------#

def energy_histogram(energy_bound, tally_result, savepath,
        plot_title='',
        x_title='Energy Bins (MeV)', y_title='Tally Result',
        lowest_bin=1e-10, **kwargs):

    logger = logging.getLogger('analysis.plotting_utils.energy_hist')

    if len(energy_bound) == len(tally_result):
        logger.warning("energy groups not binned. using %s as lowest bound" %lowest_bin)
        if energy_bound[0] < lowest_bin:
            logger.warning("""lowest bin is larger than first energy bound. Enter a
                    different value""")
            return
        energy_bins = np.append([lowest_bin],energy_bound)
    else:
        energy_bins = energy_bound
    pseudodata = energy_bins[1:]*.99
    sns.set_style("ticks",
            {"ytick.direction": u'in',
             "xtick.direction": u'in'})
    # sns.set(rc={'text.usetex' : True})
    if savepath is not None:
        fig = plt.figure()
    plt.hist(pseudodata, bins=energy_bins, weights=tally_result,
            histtype='step', fill=False, linewidth=1, **kwargs)
    if plot_title:
        plt.title('%s' %plot_title)
    plt.xlabel('%s' %x_title)
    plt.ylabel('%s' %y_title)
    plt.xscale('log')
    if savepath is not None:
        plt.savefig('%s' %(savepath), hbox_inches='tight')
        plt.close(fig)
    else:
        return plt

def boxbyenergy(data, plot_title, x_title, y_title, savepath, log_scale=False):
    plot_title = str(plot_title)
    x_title = str(x_title)
    y_title = str(y_title)

    sns.set_style("whitegrid")
    fig = plt.figure(figsize=(15,5))
    pal = sns.diverging_palette(10, 240, n=27)
    sns.boxplot(data=data, palette=pal, linewidth=1.25)
    plt.title(plot_title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    if log_scale==True:
        plt.yscale('log')
    plt.savefig('%s' %(savepath), hbox_inches='tight')
    plt.close(fig)

def violinbyenergy(data, plot_title, x_title, y_title, savepath,
        log_scale=False):
    plot_title = str(plot_title)
    x_title = str(x_title)
    y_title = str(y_title)

    sns.set_style("whitegrid")
    fig = plt.figure(figsize=(15,5))
    pal = sns.diverging_palette(10, 240, n=27)
    sns.violinplot(data=data, palette=pal, bw=.2, cut=0, linewidth=1, log_bins=True)
    plt.title(plot_title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    if log_scale == True:
        plt.yscale('log')
    plt.savefig('%s' %(savepath), hbox_inches='tight')
    plt.close(fig)

def stripbyenergy(data, plot_title, x_title, y_title, savepath, log_scale=False):
    plot_title = str(plot_title)
    x_title = str(x_title)
    y_title = str(y_title)

    sns.set_style("whitegrid")
    fig = plt.figure(figsize=(15,5))
    pal = sns.diverging_palette(10, 240, n=27)
    sns.stripplot(data=data, palette=pal, jitter=True, size=1)
    plt.title(plot_title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    if log_scale == True:
        plt.yscale('log')
    plt.savefig('%s' %(savepath), hbox_inches='tight')
    plt.close(fig)

def violinbymetric(data, plot_title, x_title, x_names, y_title, savepath,
        log_scale=False):
    sns.set_style("whitegrid")
    fig = plt.figure(figsize=(10,5))
    if log_scale == True:
        plt.yscale('log')
    pal=sns.color_palette("YlOrRd", 16)
    sns.violinplot(data=data, palette=pal[8:], linewidth=1, cut=0,
                   scale='width', gridsize=100, inner='box', log_bins=True,
                   bw=.2)
    plt.title(plot_title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.xticks(np.arange(len(names)),names, rotation=45)
    plt.gcf().subplots_adjust(bottom=0.20)
    plt.savefig('%s' %(savepath), hbox_inches='tight')
    plt.close(fig)

def stripbymetric(data, plot_title, x_title, x_names, y_title, savepath,
        log_scale=False):
    sns.set_style("whitegrid")
    fig = plt.figure(figsize=(10,5))
    pal=sns.color_palette("YlOrRd", 16)
    if log_scale == True:
        plt.yscale('log')
    sns.stripplot(data=data, palette=pal[8:], jitter=True, size=1)
    plt.title(plot_title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.xticks(np.arange(len(names)), names, rotation=45)
    plt.gcf().subplots_adjust(bottom=0.20)
    plt.savefig('%s' %(savepath), hbox_inches='tight')
    plt.close(fig)

def boxbymetric(data, plot_title, x_title, x_names, y_title, savepath,
        log_scale=False):
    sns.set_style("whitegrid")
    fig = plt.figure(figsize=(10,5))
    pal=sns.color_palette("YlOrRd", 16)
    if log_scale == True:
        plt.yscale('log')
    sns.boxplot(data=data, palette=pal[8:], linewidth=1)
    plt.title(plot_title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.xticks(np.arange(len(names)), names, rotation=45)
    plt.gcf().subplots_adjust(bottom=0.20)
    plt.savefig('%s' %(savepath), hbox_inches='tight')
    plt.close(fig)

def statscatter(x1, x2, x4, y, savepath, metric_name='default metric name',
                y_name='Tally Relative Error', pal='groups', scale='linear'):
    '''This plot is not going to be particularly flexible. It will
    return a line of several plots that show the correlation between a single y
    dataset and the mean (x1), median (x2), mean/median (x1/x2), and the
    variance (x4) of the anisotropy data specified.'''

    fig = plt.figure(figsize=(14,3.5))
    pal=color_palette[pal]
    title = '%s Statistics, by Energy Group, Compared to %s' %(metric_name,
            y_name)
    fig.suptitle(title)
    gs = gridspec.GridSpec(2,107)
    gs.update(wspace=0.025)
    sns.set_style("ticks",
                  {"ytick.direction": u'in',
                   "xtick.direction": u'in'})
    sns.despine()

    ax1 = fig.add_subplot(gs[:,0:21])
    ax1.scatter(x1,y, color=pal[0])
    ax1.set_ylabel(y_name)
    ax1.set_xlabel("Metric Mean Value")
    ax1.set_xscale(scale)
    if y.max()/y.min() >= 25.:
        ax1.set_yscale('log')

    ax2 = fig.add_subplot(gs[:,25:46], sharey=ax1)
    ax2.scatter(x2,y, color=pal[1])
    ax2.set_xlabel("Metric Median Value")
    ax2.set_xscale(scale)

    ax3 = fig.add_subplot(gs[:,50:71], sharey=ax1)
    ax3.scatter(x1/x2,y, color=pal[2])
    ax3.set_xlabel("Metric Mean/Median")
    ax3.set_xscale(scale)

    ax4 = fig.add_subplot(gs[:,75:96], sharey=ax1)
    ax4.scatter(x4,y, color=pal[3])
    ax4.set_xlabel("Metric Variance")
    ax4.set_xscale(scale)

    ax5 = fig.add_subplot(gs[:,100:107], sharey=ax1)
    ax5.hist(y, bins=20,
             orientation='horizontal', color=pal[4])
    ax5.get_xaxis().set_ticks([])
    ax5.yaxis.set_label_position("right")
    ax5.set_ylabel("%s Distribution" %y_name, rotation=270, labelpad=15)

    plt.subplots_adjust(top=0.87)
    plt.gcf().subplots_adjust(bottom=0.20)

    # remove the y axes labels from all plots except the first one.
    for ax in plt.gcf().axes[1:]:
        try:
            plt.setp(ax.get_yticklabels(), visible=False)
        except:
            pass
    if scale == 'linear':
        ax1.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax2.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax3.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax4.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.savefig('%s' %(savepath),bbox_inches='tight')
    plt.close(fig)

#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    main()

color_palette = {'purples':sns.cubehelix_palette(12)[5:10],
                 'groups':[sns.diverging_palette(10, 240, n=27),
                     sns.diverging_palette(10, 240, n=27),
                     sns.diverging_palette(10, 240, n=27),
                     sns.diverging_palette(10, 240, n=27),
                     '0.5'],
                 'greens':sns.cubehelix_palette(rot=-.4, n_colors=12)[4:9],
                 'purples_ex':sns.cubehelix_palette(12),
                 'g_ex': sns.color_palette("GnBu_d", n_colors=16)}

styles = {
        'cadis' : {'ls':'-.',
                   'color':color_palette['purples_ex'][6],
                   'label': 'cadis'},
        'cadisangle' : {'ls':'--',
                    'color':color_palette['purples_ex'][9],
                    'label':'cadisangle'},
        'analog' : {'ls':'-',
                     'color':color_palette['purples_ex'][3],
                     'label':'analog'},
        }

###############################################################################
# end of thesiscode/scripts/plotting_utils.py
###############################################################################
