#!/bin/bash

#######################################################################
#   Script to test PTC-PyORBIT on EOS
#######################################################################

PATHTEST="/afs/cern.ch/work/p/pyorbit/private/AFS_Phaseout_Test_2"

# The script will stop on the first error 
set -e

# Enter examples repository
cd $PATHTEST/examples/Machines/PS

PS_dir=$(pwd)

# Outputs can only be plotted when the simulations have completed tracking 25 turns
# Simulations are not complete until 500 turns are completed
Check_and_plot(){
	cd $1
	
	# check if Check_Simulation_Status.py exists in this directory
	CSS_File=Check_Simulation_Status.py
	if [[ -f "$1/$CSS_File" ]]; then
		#echo "$CSS_File exists"		
		# check if results file exists
		R_File=result.txt
		if [[ -f "$1/$R_File" ]]; then	
			#echo "$R_File exists"			
			# read contents
			file="result.txt"
			while IFS= read -r line
			do
				#echo "$line"
				if [ "$line" = 'True' ]; then
					echo
					echo simulation 
					echo "$1" 
					echo SUCCEEDED
					echo
				else
					if [ "$line" = 'False' ]; then
						echo
						echo simulation 
						echo "$1" 
						echo FAILED
						echo
					fi
				fi
			done <"$file"			
		# results file doesn't exist
		else
			# Run Check_Simulation_Status.py
			python Check_Simulation_Status.py
			# Plot outputs
			python Plot_All_Outputs.py
		fi		
	fi
	cd $PS_dir
}

# Function takes directory name only
# Assume all directories here are PyORBIT simulation tests
for d in */ ; do
	echo "Checking simulation in directory $d"
    Check_and_plot "$(pwd)/$d"
done

# Count files in a directory
# ls -1q *.mat | wc -l
