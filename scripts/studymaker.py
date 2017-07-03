###############################################################################
# File  : thesiscode/studymaker.py
# Author: madicken
# Date  : Sun Dec 18 20:11:58 2016
#
# The StudyMaker script generates a parametric study based on a specified
# (python-based) input for advantg, and then substitutes in values for the
# user-defined study. This study is one-dimensional, meaning that only one
# variable is changed per script. Should a user require multiple variables to
# be changed at once, this script will need to be updated.
###############################################################################
from __future__ import (division, absolute_import, print_function, )
#-----------------------------------------------------------------------------#
import numpy as np
import os
import re

###############################################################################

class StudyMaker(object):
    def __init__(self, filename, xs_libs = [], quad_type = [],
                 quad_order = [], pn_order = [], x_blocks = [],
                 y_blocks = [], z_blocks = []):
        '''
        The study maker takes user-defined parameters and modifies
        an advantg input file
        n number of times to include each parameter for a parametric study.
        '''
        self.filename = filename
        self.path = os.path.dirname(os.path.abspath(filename))
        self.xs_libs = xs_libs
        self.quad_type = quad_type
        self.quad_order = quad_order
        self.pn_order = pn_order
        self.x_blocks = x_blocks
        self.y_blocks = y_blocks
        self.z_blocks = z_blocks
        self.opt_dict ={}

        StudyMaker.filldictionary(self)

        StudyMaker.printopts(self)

    def printopts(self):
        '''
        Print options specified to the user after initializing the StudyMaker
        class. Pertinent information like the location of the file will also be
        generated
        '''
        print('')
        print('Option Summary')
        print('\n')
        print('advantg file :', os.path.abspath(self.filename))
        print('path :', self.path)
        print('xs_libs :', self.xs_libs)
        print('quad_types :', self.quad_type)
        print('quad_orders :', self.quad_order)
        print('pn_orders :', self.pn_order)

    def filldictionary(self):
        '''
        Fill a dictionary with the user-specified parametric study values
        and their corresponding advantg input names.
        '''
        optiondictionary = {}
        if self.xs_libs:
            name = "anisn_library"
            optiondictionary[name] = self.xs_libs
        if self.quad_type:
            name = "denovo_quadrature"
            optiondictionary[name] = self.quad_type
        if self.quad_order:
            name = "denovo_quad_order"
            optiondictionary[name] = self.quad_order
        if self.pn_order:
            name = "denovo_pn_order"
            optiondictionary[name] = self.pn_order
        if self.x_blocks:
            name = "denovo_x_blocks"
            optiondictionary[name] = self.x_blocks
        if self.y_blocks:
            name = "denovo_y_blocks"
            optiondictionary[name] = self.y_blocks
        if self.z_blocks:
            name = "denovo_z_blocks"
            optiondictionary[name] = self.z_blocks
        self.opt_dict = optiondictionary

    def printdict(self,dictionary):
        for item in dictionary:
            print(item + ':', dictionary[item])

    def changeline(self, item, value, lines):
        '''
        This function will search through the advantg input for the relevant
        variable and replace it with the new value for the study.
        '''
        patternstring = r"\"" + re.escape(item) + r"\"\:*\s.*"
        pattern = re.compile(patternstring)
        # pattern = re.compile(r"\"%s\"\:*\s.*") %item
        modified_lines = []
        for line in lines:
            if isinstance(value, int):
                line = pattern.sub('"%s":          %d,' %(item, value), line )
            elif isinstance(value, str):
                line = pattern.sub('"%s":         "%s",' %(item, value), line )
            else:
                print("%s has no instance of int or str" %(item))
            modified_lines.append(line)
        return modified_lines

    def make_study(self, newpath='', input_name=''):
        '''
        Generates a parametric study based off of the user-specified study
        variables. Each study will be contained in its own folder, named after
        the changed variable, and in that folder the relevant MCNP input will
        be copied and the edited advantg input will also be generated. If the
        MCNP input filename differs from the naem of the advantg python input,
        the user can specify it using the input_name variable. If the user
        wishes for the study base directory to be located somewhere other than
        the originating folder of the advantg sample input, this can also be
        specified with newpath.
        '''
        from shutil import copy
        f = open(self.filename, 'r')
        newpath = self.path
        lines = f.readlines()
        num_studies = 0
        for item in self.opt_dict:
            for value in self.opt_dict[item]:
                num_studies += 1
                filebase = os.path.basename(self.filename)
                input_name = os.path.splitext(filebase)[0]
                studypath = newpath+'/%s_%s' %(item,value)
                if not os.path.exists(studypath):
                    os.makedirs(studypath)
                newlines = StudyMaker.changeline(self, item, value, lines)
                newfile = os.path.join(studypath,filebase)
                nf = open(newfile, 'w')
                nf.writelines(newlines)
                copy('%s/%s' %(newpath,input_name), '%s/%s' %(studypath,input_name))
        print('%d studies created at %s' %(num_studies,newpath))

    def make_submission_script(self, input_base_file, name='', mcnpscript=False):
        '''
        Generates a PBS submission script for the parametric study. For the
        moment, this is limited to sequential runs in a single file.
        '''
        f = open(input_base_file)
        f_name = os.path.basename(input_base_file)
        if name:
            [prefix, suffix] = os.path.splitext(f_name)
            f_name = name+suffix
        else:
            f_name = os.path.splitext(f_name)[0]+'_edit'+os.path.splitext(f_name)[1]
        newpath = self.path
        edited_file = newpath+'/'+f_name
        lines = f.readlines()
        lines.append('\n')
        print('edited runscript file located at: %s' %(edited_file))
        print('lines added to file:')
        mcnpline1 = 'mkdir "./mcnp" \n'
        mcnpline2 = 'rm "./mcnp/"* \n'
        mcnpline3 = 'cp "./output/"*inp* "./mcnp/" \n'
        mcnpline4 = 'cd "./mcnp" \n'
        allmlines = mcnpline1+mcnpline2+mcnpline3+mcnpline4
        for item in self.opt_dict:
            for value in self.opt_dict[item]:
                filebase = os.path.basename(self.filename)
                studypath = newpath+'/%s_%s/' %(item,value)
                studyline1 = 'cd "%s" \n' %(studypath)
                studylinea = 'echo "Beginning PBS execution at ' + \
                        '$(date) for %s %s in $(pwd)" \n' %(item, value)
                studylineb = 'echo ">>> PBS nodes: ${PBS_NUM_NODES}" \n'
                studylinec = 'echo ">>> PBS cores per node: ${PBS_NUM_PPN}" \n'
                if mcnpscript == False:
                    studyline2 = '"${ADVANTG}" %s \n' %(filebase)
                else:
                    mcnpexec = '"${LAUNCHER}" "${MCNP}" "i=inp o=out" \n'
                    studyline2 = allmlines+mcnpexec
                studylined = 'echo ">>> Finished PBS execution for ' + \
                        '%s %s at $(date)" \n' %(item,value)
                print(studyline1, studyline2)
                lines.append(studyline1)
                lines.append(studylinea)
                lines.append(studylineb)
                lines.append(studylinec)
                lines.append(studyline2)
                lines.append(studylined)
        nf = open(edited_file, 'w')
        nf.writelines(lines)
        nf.close()

#-----------------------------------------------------------------------------#

###############################################################################
# end of thesiscode/studymaker.py
###############################################################################
