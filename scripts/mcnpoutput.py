###############################################################################
# File  : thesiscode/scripts/mcnpoutput.py
# Author: madicken
# Date  : Mon Mar 13 15:41:35 2017
#
# mcnpoutput is a series of MCNP output file reading functions.
#    -- TrackLengthTally reads an f4 tally binned by energy. It has a few
#    supplementary functions
#       - get_timing_data reads the relevant runtime information. This is
#       useful for FOM claculations
#       - get_tally_result gets the tally data and puts it into a dictionary
#       container object.
#       - get_fom_data gets the tally figure of merit statistics as a function
#       of particle count. This is relevant also for further FOM analyses.
#
###############################################################################
from __future__ import (division, absolute_import, print_function, )
#-----------------------------------------------------------------------------#
import numpy as np
import os
import re
###############################################################################

class TrackLengthTally(object):
    def __init__(self, outputpath, tallynumber='44'):
        '''
        Initialize the TrackLengthTally object, requires the tally number and
        the location of the output file
        '''

        self.outputpath = str(outputpath)
        self.tallynumber = tallynumber
        return

    def get_timing_data(self):
        '''
        This function parses out the relevant timing data for the problem. It
        will populate a dictionary with the total Monte Carlo runtime and the
        Monte Carlo transport runtimes, as well as their units.
        '''

    	time = r".*"+re.escape("computer time =")+r".*\n"
    	pattern = re.compile(time)
    	time2 = r".*"+re.escape("computer time in mcrun")+r".*\n"
    	pattern2 = re.compile(time2)

        # open the file as readonly, read in lines.
    	f = open(self.outputpath, 'r')
    	lines = f.readlines()

    	for line in lines:
            if re.match(pattern, line):
                data = line.split()
            	time = float(data[3])
            	units = data[4]
            	total_time = {'time':time,'units':units}

            elif re.match(pattern2, line):
            	data = line.split()
            	time2 = float(data[4])
            	units2 = data[5]
            	mcrun_time = {'time':time2,'units':units2}

        times = {'total_time':total_time,
                 'mcrun_time':mcrun_time}
    	return times

    def get_tally_result(self):
        '''Function used to get the tally result from the mcnp output. This
        function will return a dictionary of numpy arrays with the tally
        energy bins, the tally numerical results, and the tally relative
        errors.'''

        # read in the file
        f = open(self.outputpath, 'r')
        alllines = f.read()

        # this first regex string will pull out all of the tally data from
        # 1tally to the tally total
        str1="1tally(\s*)%s(\s*)nps(.+?)energy(.+?)total(.+?)\n"   %(self.tallynumber)
        pattern=re.compile(str1,  flags=re.DOTALL)
        results=pattern.search(alllines)

        # now we'll clean out the data to contain just the numerical results
        # of the tally
        numbers = re.compile("energy(.+?)total(.+?)\n", flags=re.DOTALL)
        allnums = numbers.search(results.group(0))
        splitlines= allnums.group(0).splitlines()
        groups = np.array([])
        tally = np.array([])
        relative_error = np.array([])

        # now we'll loop through the lines and put the tally results into numpy arrays
        for i in range(len(splitlines)-2):

            # we're skipping line[0] because it starts with the energy string
            splitsplitlines = splitlines[i+1].split()
            groups = np.append(groups, float(splitsplitlines[0]))
            tally = np.append(tally, float(splitsplitlines[1]))
            relative_error = np.append(relative_error, float(splitsplitlines[2]))

        # The last line of the tally result is the tally total result and tally
        # total relative error. We don't want this messing with our results so
        # we'll save it to different variable information.
        last_line = splitlines[-1].split()
        tally_total, tally_re = float(last_line[1]), float(last_line[2])

        # put the tally data into a dict
        tally_data = {'energy_groups':groups,
                      'tallied_result':tally,
                      'relative_error':relative_error,
                      'tallied_total' :tally_total,
                      'tally_total_relative_error':tally_re}
        return tally_data


    def get_fom_data(self):
        '''
        Function that scrapes specified tally statistical results, including
        the tally variance, the tally slope, the tally total relative error,
        the tally Figure of Merit (FoM), and the particle count associated
        with each. The funciton will return a dictionary with key value pairs
        with labels and corresponding numpy arrays.
        '''

        # read in the file
        f = open(self.outputpath, 'r')
        alllines = f.read()

        # First pull in the fom data for the specified tally number including
        # tally header information.
        str1="1tally(\s*)fluctuation(\s*)charts(.+?)tally(\s*)%s(.+?)dump(.+?)" %(self.tallynumber)
        pattern=re.compile(str1,  flags=re.DOTALL)
        results=pattern.search(alllines)

        # Now pull out the specific tally numerical results for the FOM and
        # particle count from that tally
        str2='nps(.+?)\n(\s*)\n'
        pattern = re.compile(str2, flags=re.DOTALL)
        tally_data=pattern.search(results.group(0))
        tally_data=tally_data.group(0).splitlines()

        # generate a set of empty numpy arrays to populate when reading in the
        # tally information.
        particle_count = np.array([])
        tally_mean = np.array([])
        tally_error = np.array([])
        tally_vov = np.array([])
        tally_slope = np.array([])
        tally_fom = np.array([])

        for item in range(len(tally_data)-1):
            splitresults = tally_data[item].split()

            # The first line we read in is the labels for each column. Don't
            # include this information in the aformentioned numpy arrays but
            # save it in the tally_labels variable
            if item == 0:
                tally_labels = splitresults

            # Populate the other numpy arrays with the tally data
            else:
                tally_mean = np.append(tally_mean, float(splitresults[1]))
                tally_error = np.append(tally_error, float(splitresults[2]))
                tally_vov = np.append(tally_vov, float(splitresults[3]))
                tally_slope = np.append(tally_slope, float(splitresults[4]))
                tally_fom = np.append(tally_fom, float(splitresults[5]))
                particle_count = np.append(particle_count, float(splitresults[0]))


        # Put all of the tally data into a container dictionary
        tally_trends = {tally_labels[0]:particle_count,
                        tally_labels[1]:tally_mean,
                        tally_labels[2]:tally_error,
                        tally_labels[3]:tally_vov,
                        tally_labels[4]:tally_slope,
                        tally_labels[5]:tally_fom}

        return tally_trends



#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    main()

###############################################################################
# end of thesiscode/scripts/mcnpoutput.py
###############################################################################
