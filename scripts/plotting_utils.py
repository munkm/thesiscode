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
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib import gridspec
###############################################################################

# Default Values for various things

names = [u'adjoint_anisotropy', u'forward_anisotropy', u'metric_five',
u'metric_four', u'metric_one', u'metric_six', u'metric_three', u'metric_two']


#-----------------------------------------------------------------------------#


def energy_histogram(energy_bound, tally_result, savepath, plot_title='default title',
        x_title='Energy Bins (MeV)', y_title='Tally Result',
        color='#412966', lowest_bin=1e-10):
    if len(energy_bound) == len(tally_result):
        print("energy groups not binned. using %s as lowest bound" %lowest_bin)
        if energy_bound[0] < lowest_bin:
            print("""lowest bin is larger than first energy bound. Enter a
                    different value""")
            return
        energy_bins = np.append([lowest_bin],energy_bound)
    else:
        energy_bins = energy_bound
    pseudodata = energy_bins[1:]*.99
    sns.set_style("ticks",
            {"ytick.direction": u'in',
             "xtick.direction": u'in'})
    plt.hist(pseudodata, bins=energy_bins, weights=tally_result,
            histtype='step', fill=False, linewidth=1, color=color)
    plt.title('%s' %plot_title)
    plt.xlabel('%s' %x_title)
    plt.ylabel('%s' %y_title)
    plt.xscale('log')
    plt.savefig('%s' %(savepath), hbox_inches='tight')

def boxbyenergy(data, plot_title, x_title, y_title, savepath, log_scale=False):
    plot_title = str(plot_title)
    x_title = str(x_title)
    y_title = str(y_title)

    sns.set_style("whitegrid")
    plt.figure(figsize=(12,5))
    if log_scale==True:
        plt.yscale('log')
    pal = sns.diverging_palette(10, 240, n=27)
    sns.boxplot(data=data, palette=pal, linewidth=1.25)
    plt.title(plot_title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.savefig('%s' %(savepath), hbox_inches='tight')

def violinbyenergy(data, plot_title, x_title, y_title, savepath):
    plot_title = str(plot_title)
    x_title = str(x_title)
    y_title = str(y_title)

    sns.set_style("whitegrid")
    plt.figure(figsize=(15,5))
    pal = sns.diverging_palette(10, 240, n=27)
    sns.violinplot(data=data, palette=pal, bw=.2, cut=0, linewidth=1, log_bins=True)
    plt.title(plot_title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.yscale('log')
    plt.savefig('%s' %(savepath), hbox_inches='tight')

def violinbygroup(data, plot_title, x_title, x_names, y_title, savepath):
    sns.set_style("whitegrid")
    plt.figure(figsize=(10,5))
    plt.yscale('log')
    pal=sns.color_palette("YlOrRd", 16)
    sns.violinplot(data=data[:,1:], palette=pal[8:], linewidth=1, cut=0,
                   scale='width', gridsize=100, inner='box', log_bins=True,
                   bw=.2)
    plt.title(plot_title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.xticks(np.arange(len(names)),names, rotation=45)
    plt.gcf().subplots_adjust(bottom=0.20)
    plt.savefig('%s' %(savepath), hbox_inches='tight')

def stripbygroup(data, plot_title, x_title, x_names, y_title, savepath):
    sns.set_style("whitegrid")
    plt.figure(figsize=(10,5))
    pal=sns.color_palette("YlOrRd", 16)
    plt.yscale('log')
    sns.stripplot(data=data, palette=pal[8:], jitter=True, size=1)
    plt.title(plot_title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.xticks(np.arange(len(names)), names, rotation=45)
    plt.gcf().subplots_adjust(bottom=0.20)
    plt.savefig('%s' %(savepath), hbox_inches='tight')

def statscatter(x1, x2, x4, y, savepath, metric_name='default metric name',
                y_name='Tally Relative Error'):
    '''This particular plot is not going to be particularly flexible. It will
    return a line of several plots that show the correlation between a single y
    dataset and the mean (x1), median (x2), mean/median (x1/x2), and the
    variance (x4) of the anisotropy data specified.'''

    fig = plt.figure(figsize=(14,3.5))
    pal=sns.cubehelix_palette(12)
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
    ax1.scatter(x1,y, color=pal[6])
    ax1.set_ylabel(y_name)
    ax1.set_xlabel("Mean Value")

    ax2 = fig.add_subplot(gs[:,25:46])
    ax2.scatter(x2,y, color=pal[7])
    ax2.get_yaxis().set_ticklabels([])
    ax2.set_xlabel("Median Value")


    ax3 = fig.add_subplot(gs[:,50:71])
    ax3.scatter(x1/x2,y, color=pal[8])
    ax3.get_yaxis().set_ticklabels([])
    ax3.set_xlabel("Mean/Median")

    ax4 = fig.add_subplot(gs[:,75:96])
    ax4.scatter(x4,y, color=pal[9])
    ax4.get_yaxis().set_ticklabels([])
    ax4.set_xlabel("Metric Variance")

    ax5 = fig.add_subplot(gs[:,100:107])
    ax5.hist(y, bins=15,
    orientation='horizontal', color=pal[10])
    ax5.get_yaxis().set_ticklabels([])
    ax5.get_xaxis().set_ticks([])
    ax5.yaxis.set_label_position("right")
    ax5.set_ylabel("%s Distribution" %y_name, rotation=270, labelpad=15)

    plt.subplots_adjust(top=0.87)
    plt.gcf().subplots_adjust(bottom=0.20)
    plt.setp(ax.get_xticklabels(), rotation=30
    plt.savefig('%s' %(savepath),bbox_inches='tight')

#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    main()

###############################################################################
# end of thesiscode/scripts/plotting_utils.py
###############################################################################
