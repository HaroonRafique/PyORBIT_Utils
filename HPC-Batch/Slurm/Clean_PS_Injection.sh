#!/bin/bash
for directory in $(find PS_Injection -type d); 
do
    echo "$directory";
    rm flat.dat
    rm -r input
    rm -r output
    rm Negative_node.OUT
    rm ptc_twiss
    rm simulation_parameters.pyc
    rm SPACE_CHARGE_STUDIES_INJECTION.flt
    rm junk.txt
    rm Maxwellian_bend_for_ptc.txt
done


