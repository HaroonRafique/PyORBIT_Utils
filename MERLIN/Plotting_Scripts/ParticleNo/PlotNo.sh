#
# GNUPLOT script to plot survived percentage for TevHEL
#
set terminal png size 2400,800
set output "HL_HEL_Survival.png"
set multiplot layout 1,3 title "Final Bunch" font ",14"
# original
#~ NH="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/TevHEL/09Feb16_TeV_NH/ParticleNo"
#~ DC="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/TevHEL/09Feb16_TeV_DC/ParticleNo"
#~ AC="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/TevHEL/09Feb16_TeV_AC/ParticleNo"
#~ DIFF="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/TevHEL/09Feb16_TeV_DIFF/ParticleNo"
#~ ACL="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/TevHEL/09Feb16_TeV_LHC_AC/ParticleNo"
#~ DCL="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/TevHEL/09Feb16_TeV_LHC_DC/ParticleNo"
#~ DIFFL="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/TevHEL/09Feb16_TeV_LHC_DIFF/ParticleNo"
#reruns
NH="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELFullBeam/19FebTest_NH/ParticleNo"
DC="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELFullBeam/19FebTest_DC/ParticleNo"
AC="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELFullBeam/19FebTest_AC/ParticleNo"
DIFF="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELFullBeam/19FebTest_DIFF/ParticleNo"
core="/Core/No.txt"
halo="/Halo/No.txt"
npart=1e3
cpart=1e2
turns=1E3
zoomturns=1E2
#
set tmargin 3
set title "HL Halo"
set yrange[0.65:1]
set xrange[0:turns]
set xlabel "Turn [-]"
set ylabel "N/N_0[-]"
plot (NH.halo) u 1:($2/npart) title "NH" lt 8, (DC.halo) u 1:($2/npart) title "DC" lt 2, (AC.halo) u 1:($2/npart) title "AC" lt 7, (DIFF.halo) u 1:($2/npart) title "DIFF" lt 4
#
#
unset key
#
set tmargin 3
set title "HL Halo Zoom"
set yrange[0.85:1]
set xrange[0:zoomturns]
set xlabel "Turn [-]"
set ylabel "N/N_0[-]"
plot (NH.halo) u 1:($2/npart) title "NH" lt 8, (DC.halo) u 1:($2/npart) title "DC" lt 2, (AC.halo) u 1:($2/npart) title "AC" lt 7, (DIFF.halo) u 1:($2/npart) title "DIFF" lt 4
#
#
unset key
#
set tmargin 3
set title "HL Core"
set yrange[0.99:1.01]
set xrange[0:turns]
set xlabel "Turn [-]"
set ylabel "N/N_0[-]"
plot (NH.core) u 1:($2/cpart) title "NH" lt 8, (DC.core) u 1:($2/cpart) title "DC" lt 2, (AC.core) u 1:($2/cpart) title "AC" lt 7, (DIFF.core) u 1:($2/cpart) title "DIFF" lt 4
#
#
unset key
#
unset multiplot
#

