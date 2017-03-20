###############################################################################
# File  : thesiscode/scripts/analysis.py
# Author: madicken
# Date  : Tue Mar 14 14:05:05 2017
#
# <+Description+>
###############################################################################
from __future__ import (division, absolute_import, print_function, )
#-----------------------------------------------------------------------------#
import numpy as np
from mcnpoutput import TrackLengthTally
from matplotlib import pyplot as plt
import seaborn as sns
###############################################################################

class MCNPoutput(object):
    def __init__(self, outputlocation, tallynumber='44'):
        self.ouputlocation = str(outputlocation)
        self.title = self.outputlocation
        self.tallynumber = tallynumber
        pass

    def get_tally_data(self):
        output_init = TrackLengthTally(self.outputlocation, self.tallynumber)
        output_fom = output_init.get_fom_data()
        output_tally = output_init.get_tally_result()
        output_timing = output_init.get_timing_data()
        output_container = {'timing' : output_timing,
                            'fom_trends' : output_fom,
                            'tally_data' : output_tally}
        return output_container

    def plot_tally_fom(self):
        pass


#-----------------------------------------------------------------------------#

class Anisotropy(object):
    def __init__(self):
        pass

#-----------------------------------------------------------------------------#

class FOMdata(output):
    def __init__(self):
        pass

    def

#-----------------------------------------------------------------------------#

###############################################################################
# end of thesiscode/scripts/analysis.py
###############################################################################
