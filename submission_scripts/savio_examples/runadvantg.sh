#!/bin/bash
# job name:
#SBATCH --job-name=adv_run
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
# QoS:
#SBATCH --qos=nuclear_normal
#
#SBATCH --output=slurm_%j.out
#SBATCH --error=slurm_%j.err
## Run command
advantg run_name.py
