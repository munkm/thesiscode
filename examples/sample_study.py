from studymaker import StudyMaker

C = StudyMaker('/home/m15/munk_analysis/angle/prob_1_finer/cadis/prob_1.py', \
        quad_order = [5, 7, 10, 12, 15, 17, 20], pn_order = [1,3,5])

# This will open prob_1.py (the advantg input), make folders for each pn_order
# and each quad_order, and then write the modified prob_1.py files to each
# folder.
C.make_study()

# Based on the directory structure that is defined, this will make a pbs
# submission script using the header from runall.pbs and save it at
# cadisstudy.pbs for an advantg run with all of the inputs
# defined in make_study.
C.make_submission_script('/home03/m15/munk_analysis/angle/prob_1/cadis/runall.pbs', name='cadisstudy')

# Based on the directory structure that is defined, this will make a pbs
# submission script using the header from runmcnp.pbs and save it at
# mcnpstudy.pbs for an mcnp run with all of the inputs
# defined in make_study.
C.make_submission_script('/home03/m15/munk_analysis/angle/prob_1/cadis/runmcnp.pbs', name='mcnpstudy', mcnpscript=True)

