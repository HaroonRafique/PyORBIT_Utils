#
# GNUPLOT script to HEL footprint with HEL beam 
# assumes initial bunch is at the HEL
#
set terminal png size 800,800
set output "HEL_Footprint_with_Initial_Bunch.png"
#
HEL="/home/HR/Downloads/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELFullBeam/16FebTest/HEL/footprint.txt"
B="/home/HR/Downloads/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELFullBeam/16FebTest/Bunch_Distn/Halo/initial_bunch.txt"
#
set title "HEL Footprint"
#~ set yrange[0.65:1]
#~ set xrange[0:turns]
set xlabel "x [m]"
set ylabel "y [m]"
plot HEL u 1:2 title "HEL", B u 3:5 title "Bunch"
#
