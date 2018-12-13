#!/bin/bash
# condor cleanup
rm output/simulation_info_* 
rm logfile_*
rm output_*
# clean ghost files
rm Input/mainbunch_start.dat~
rm Input/optics_ptc.txt~
rm Input/time.ptc~
rm Input/ParticleDistribution.in~
# ptc cleanup
rm flat.dat
rm junk.txt
rm Maxwellian_bend_for_ptc.txt
rm SPACE_CHARGE_STUDIES_INJECTION.flt
rm ptc_twiss
rm Negative_node.OUT
# PyORBIT cleanup
rm simulation_parameters.pyc
rm -r input/
rm -r bunch_output/mainbunch*
rm output/output.mat
