## Directions for executing advantg and MCNP on Savio

#### Files in this folder:
* `runadvantg.sub` shell script to run advantg
  * All of the lines starting with a # in this file are things used by the
    SLURM submission to allocate job size. Based in the comments of the file,
    you should be able to deduce what job size you need. If you're comparing
    different runs in advantg, you should generally not change these variables
    between runs, since changing the computational resources will change the
    nature of the job.
  * The last line of this file has the actual execution of ADVANTG. You can see
    we choose to execute with a .py file. However, if you have a .adv advantg
    formatted file, you can also modify the `advantg run_name.py` to `advantg run_name.adv`
  * If this script fails, check to see that you have advantg properly being
    called by executing `$ which advantg`. On my user profile on savio, this
    returns 
      ```
      $ which advantg
      /global/home/groups/co_nuclear/ADVANTG/bin/advantg
      ```
    which should be the same for you.
* `runmcnp.sub` shell script to run mcnp
  * All of the lines starting with a # in this file are things used by the
    SLURM submission to allocate job size. Based in the comments of the file,
    you should be able to deduce what job size you need. If you're comparing
    different variations in MCNP input (like particle count) from a single
    advantg run, you should generally not change these variables
    between runs, since changing the computational resources will change the
    nature of the job.
  * The last two lines of this file have the actual execution of MCNP. Make
    sure you execute the MCNP submission using the actual edited MCNP file that
    advantg generates. This should be located in `./output/` of the advantg run
    folder. The lines to run MCNP are:
       ```
       module load openmpi
       mpirun mcnp5_151.mpi i=inp 
       ```
    The first line loads the mpi module, which is used to launch parallel jobs.
    This is required to run any .mpi compiled version of a software, including
    MCNP version 5.151. Then mpirun is used to launch MCNP in the second line.
    The input file (named inp generically here) is designated 
    with `i=inp`. You can also designate an output
    with `o=out` (named out generically here). 
* `bash_additions.rc` file with environment variables that need to be added to
  the `.bashrc` file located in your user $HOME directory on savio. Make sure
  to edit your .bashrc file before you try to use either runmcnp.sub or
  runadvantg.sub

#### Submitting a job:

* A MCNP job:
  * **to submit**: execute `$ sbatch runmcnp.sub`
  * **to check status**: execute `squeue -u` 
    * This will list all of the jobs in the submission queue under your
      username. 
  * **to cancel**: execute `scancel 12345` where 12345 is the job ID#
    * To get the job ID number, look in the first column of squeue. Here's an
      example:
      ```
          JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
           1838787    savio2 a1508537 bracewel PD       0:00      1 (JobHeldUser)
           1838864    savio2 a1508537 bracewel PD       0:00      1 (JobHeldUser)
           1838960    savio2 a1508538 bracewel PD       0:00      1 (JobHeldUser)
           1838984    savio2 a1508538 bracewel PD       0:00      1 (JobHeldUser)
      ```

* An ADVANTG job:
  * **to submit**: execute `$ sbatch runadvantg.sub`
  * **to check status**: see above
  * **to cancel**: see above

#### Other useful things:

* The savio documentation on submissions is here:
  http://research-it.berkeley.edu/services/high-performance-computing/running-your-jobs
  It is well-documented and has many examples. 
* Interactive jobs are useful if you want to make sure an MCNP run is working
  as you expect and you can watch it run in real time. Its also slower because
  of screen printing, so don't use it for all of your jobs. 
* The `.sub` scripts in this folder are used to run a single advantg or mcnp run
  at a time. The ones in the folder above this are used to run several in
  sequence. You can use them as references to make more sophisticated scripts
  as you see fit. The lines without # symbols are shell scripts, so they should
  execute similarly between different job submission software.
* If for whatever reason you can't find MCNP or advantg after modifying your
  .bashrc file try the following:
  * executing `$ source ~/.bashrc` 
    * this will re-source your modified bashrc file. If you are trying to run
      MCNP or ADVANTG in the same session taht you modified this file, you need
      your environment to be updated.
  * executing `$ groups` 
    * For my user profile on savio, this results in:
        ```
        $ groups
        ucb savio savio_scaledev savio_mcnp savio_scale6 savio_scale6b
        savio_exnihilo savio_advantg co_nuclear fc_neutronics
        ```
      If you are not in `savio_mcnp` or `savio_advantg`, contact rachel or max
      to get added. 

