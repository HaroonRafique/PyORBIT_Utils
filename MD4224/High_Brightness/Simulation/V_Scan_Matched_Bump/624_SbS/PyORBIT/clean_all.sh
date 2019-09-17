#!/bin/bash
# This script will clean ALL simulation files generated in PyORBIT
# Do not run unless you wish to start the simulation from scratch
rm *.png
rm optics.txt
rm optics_2.txt
rm SLURM_submission_script.sh
rm Orbit_Extrema.dat
. clean_run.sh
. clean_junk.sh
