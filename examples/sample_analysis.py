from compare_runs import Compare_Runs
from single_run import Single_Run

# The problems dictionary. Because I used a dict structure, I can assign the
# folder name 'beam' to the name that I want used in the figures (which is more
# descriptive). Here it is 'Beam Facility'. Also, because I do a
# problems.iteritems() lower down to start the analysis I can have MULTIPLE
# problem and folder names included in this dictionary to perform the same
# analysis on all of these problems.

problems = {
            'beam': 'Beam Facility',
        }

# This list will choose with which portion of the anisotropy data to perform the
# statistical analyses of the anisotropy.
selection = ['full', 'median', 'mean']
# selection = ['full']

for key,value in problems.iteritems():
    print('Running compare analysis for %s' %(value))

    # Initializes the compare_runs object. This will pull in the directory
    # structure and file locations for cadisangle, cadis, and the analog run.
    run = Compare_Runs(cadisanglefolder='~/munk_analysis/demonstration/cadisangle/%s/' %(key),
            cadisfolder='~/munk_analysis/demonstration/cadis/%s/' %(key),
            analogfolder='~/munk_analysis/demonstration/analog/%s/' %(key),
            problem_name='%s' %(value))

    # This will generate the tally relative error and the FOM improvement
    # factors (the ratio of cadisangle to cadis) as a function of the
    # anisotropy statistics. An example with Metric 3 can be found in Figure
    # 4.11 (a) through (c) in my dissertation.
    run.do_compare_analysis(
            plot_compare_corrs=True,
            plot_compare_corrs_median=True,
            plot_compare_corrs_mean=True)

    # This will generate the tally results, the tally relative errors, generate
    # a .tex table for the timing, the figure of merits, and the tally
    # convergence results that compare all of the folders defiend in
    # Compare_Runs. Here that is analog, cadis, and cadisangle. (e.g. Fig 4.7
    # (a) and (b) in my dissertation)
    run.do_compare_analysis(plot_tally_results=True, plot_tally_error=True,
            make_timingtable=True, make_fomtable=True,
            make_tallytable=True, saveformat='tex')

    # This will generate the anisotropy data for the problem. Because the
    # anisotropy data is defined by the metrics in my dissertation, they
    # require the full angular flux information, which is only in the
    # cadisangle run. As a result, we only need the cadisangle folder here.
    run2 = Single_Run('~/munk_analysis/demonstration/cadisangle/%s/'
            %(key), method_type='cadisangle')
    for select in selection:
        # because selection is the list of full, mean, and median defined above
        # this particular loop will generate box and violin plots for each
        # metric (again defined in my thesis) based on selections of the
        # anisotropy data. (e.g. fig 4.9 (b) and (c) of my dissertation are
        # examples of a box and a violin plot. Fig 4.10 shows how the violin
        # plot changes as a function of different data selections.)
        run2.do_single_analysis(
                plot_boxes_for_metric=True, plot_violins_for_metric=True,
                select_anisotropies='%s' %(select))
