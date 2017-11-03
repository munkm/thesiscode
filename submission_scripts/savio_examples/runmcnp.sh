#!/bin/bash
# job name:
#SBATCH --job-name=mcnp_run
#
# Partition:
#SBATCH --partition=savio
#
# Wall clock limit:
#SBATCH --time=05:00:00
#
# Processors:
#SBATCH --ntasks=20
#
# Account:
#SBATCH --account=co_nuclear
#
#SBATCH --qos=nuclear_normal
#SBATCH --output=tests.out
#SBATCH --error=test.err
## Run command
module load openmpi
mpirun mcnp5_151.mpi i=inp 
