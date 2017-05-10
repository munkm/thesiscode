###############################################################################
# File  : thesiscode/anisotropy.py
# Author: madicken
# Date  : Tue Jan 03 13:00:02 2017
#
# <+Description+>
###############################################################################
#-----------------------------------------------------------------------------#
import numpy as np
import h5py
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import os

###############################################################################

class AnisotropyAnalysis(object):
    def __init__(self, path):
        self.path = str(path)
        return

    def get_paths(self, filename='problem_anisotropies.h5'):
        self.path = os.path.abspath(self.path)
        # check if hdf5 file exists in subdirectory
        if os.path.isfile('%s/%s'
                %(self.path, filename)):
            filepath = '%s/%s' %(self.path,filename)
            newdir = '%s/anisotropy_figures' %(self.path)
            os.makedirs(newdir)
        elif os.path.isfile('%s/omega_solution/%s'
                %(self.path, filename)):
            filepath = '%s/omega_solution/%s' %(self.path, filename)
            newdir = '%s/omega_solution/anisotropy_figures'
            os.makedirs(newdir)
        else:
            print('cannot find %s in subdirectories here' %(filename))
        longpathname = filepath
        path_to_file = os.path.abspath(longpathname)

        return(longpathname, path_to_file, newdir)

    def get_data(self, filename):
        filename = str(filename)
        data = {}
        with h5py.File(filename, 'r') as hfile:
            datasetnames = hfile.keys()
            for name in datasetnames:
                newname = name.encode('utf8')
                datasets = hfile.get(newname).items()
                for name2,value in datasets:
                    matrix = np.array(value)
                    newestname = name+'_'+name2
                    newestname.encode('utf8')
                    data['%s' %(newestname)] = matrix
        return data

    def plot_histogram_of_metric(self,plotname,savepath,data):
        path = str(path)
        n, bins, patches = plt.hist(data, bins=50, normed=1,
                facecolor='#90D4BB')
        plt.xlabel('Ratio')
        plt.ylabel('Frequency')
        plt.yscale('log')
        plt.title(r'Histogram of %s' %(name))
        plt.grid(True)
        plt.savefig('%s/%s.pdf' %(savepath,plotname), hbox_inches='tight')
        plt.close()


#-----------------------------------------------------------------------------#

###############################################################################
# end of thesiscode/anisotropy.py
###############################################################################
