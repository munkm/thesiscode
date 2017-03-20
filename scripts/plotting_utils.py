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
    # plt.show()
    plt.close()



#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    main()

###############################################################################
# end of thesiscode/scripts/plotting_utils.py
###############################################################################
