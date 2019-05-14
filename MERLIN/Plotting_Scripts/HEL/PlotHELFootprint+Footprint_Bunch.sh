#
# GNUPLOT script to HEL footprint with HEL beam 
# assumes initial bunch is at the HEL
#
set terminal png size 800,800
set output "HEL_Footprint_with_Initial_Bunch.png"
#
HEL="/home/HR/Downloads/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELFullBeam/23Feb_Elliptical_Footprint_DC/HEL/footprint.txt"
H="/home/HR/Downloads/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELFullBeam/23Feb_Elliptical_Footprint_DC/Bunch_Distn/Halo/HEL_bunch.txt"
C="/home/HR/Downloads/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELFullBeam/23Feb_Elliptical_Footprint_DC/Bunch_Distn/Halo/HEL_bunch.txt"
#
set title "HEL Footprint 100 turns"
#~ set yrange[0.65:1]
#~ set xrange[0:turns]
set xlabel "x [m]"
set ylabel "y [m]"
plot HEL u 1:2 title "HEL" lt 8, H u 3:5 title "Halo" lt 2, C u 3:5 title "Core" lt 7
#
