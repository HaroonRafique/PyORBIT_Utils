#!/bin/bash

#######################################################################
#   Script to test PTC-PyORBIT on EOS
#######################################################################

PATHTEST="/afs/cern.ch/work/p/pyorbit/private/AFS_Phaseout_Test_1"

# The script will stop on the first error 
set -e

# Enter examples repository
cd $PATHTEST/examples/Machines/PS

PS_dir=$(pwd)

# Outputs can only be plotted when the simulations have completed tracking 25 turns
# Simulations are not complete until 500 turns are completed
Check_and_plot(){
	cd $1
	# Check if simulation has completed
	python Check_Simulation_Status.py
	# Plot outputs
	python Plot_All_Outputs.py
	cd $PS_dir
}

# Function takes directory name only
# Assume all directories here are PyORBIT simulation tests
for d in */ ; do
	echo "Checking simulation in directory $d"
    Check_and_plot "$d"
done
