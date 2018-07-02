#!/bin/bash
rm flat.dat
rm junk.txt
rm Maxwellian_bend_for_ptc.txt
rm SPACE_CHARGE_STUDIES_INJECTION.flt
rm ptc_twiss
rm Negative_node.OUT
rm simulation_parameters.pyc
rm -r input/
rm -r bunch_output/mainbunch*
mkdir Condor_Logfiles
mv logfile_* Condor_Logfiles
mv output_* Condor_Logfiles
