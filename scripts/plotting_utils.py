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
###############################################################################

# Default Values for various things

names = [u'adjoint_anisotropy', u'forward_anisotropy', u'metric_five',
u'metric_four', u'metric_one', u'metric_six', u'metric_three', u'metric_two']


#-----------------------------------------------------------------------------#


def energy_histogram(energy_bound, tally_result, title='default title',
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
    plt.title('%s' %title)
    plt.xlabel('Energy Bins (MeV)')
    plt.ylabel('Relative Error')
    plt.xscale('log')
    plt.savefig('/Users/madicken/Documents/wwdebug/sillyplot.png', hbox_inches='tight')

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


#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    main()

###############################################################################
# end of thesiscode/scripts/plotting_utils.py
###############################################################################
