#!/bin/bash
rm flat.dat
rm junk.txt
rm Maxwellian_bend_for_ptc.txt
rm SPACE_CHARGE_STUDIES_INJECTION.flt
rm ptc_twiss
rm Negative_node.OUT
rm simulation_parameters.pyc
rm -r bunch_output/mainbunch*
mkdir Condor_Logfiles
mv input/simulation_info_* Condor_Logfiles
rm -r input/
mv logfile_* Condor_Logfiles
mv output_* Condor_Logfiles
