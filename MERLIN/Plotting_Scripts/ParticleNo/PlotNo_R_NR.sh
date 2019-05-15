#
# GNUPLOT script to plot survived percentage for TevHEL
#
set terminal png size 2400,800
set output "HL_HEL_Survival.png"
set multiplot layout 2,3 title "Final Bunch" font ",14"
# original
#~ NH="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/TevHEL/09Feb16_TeV_NH/ParticleNo"
#~ DC="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/TevHEL/09Feb16_TeV_DC/ParticleNo"
#~ AC="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/TevHEL/09Feb16_TeV_AC/ParticleNo"
#~ DIFF="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/TevHEL/09Feb16_TeV_DIFF/ParticleNo"
#~ ACL="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/TevHEL/09Feb16_TeV_LHC_AC/ParticleNo"
#~ DCL="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/TevHEL/09Feb16_TeV_LHC_DC/ParticleNo"
#~ DIFFL="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/TevHEL/09Feb16_TeV_LHC_DIFF/ParticleNo"
#reruns
NHR="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELFullBeam/19FebTest_NH/ParticleNo"
DCR="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELFullBeam/19FebTest_DC/ParticleNo"
ACR="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELFullBeam/19FebTest_AC/ParticleNo"
DIFFR="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELFullBeam/19FebTest_DIFF/ParticleNo"
NHNR="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELFullBeam/19FebTest_NH_NR/ParticleNo"
DCNR="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELFullBeam/19FebTest_DC_NR/ParticleNo"
ACNR="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELFullBeam/19FebTest_AC_NR/ParticleNo"
DIFFNR="/home/haroon/MERLIN_HRThesis/MERLIN/Build/Thesis/outputs/HELFullBeam/19FebTest_DIFF_NR/ParticleNo"
core="/Core/No.txt"
halo="/Halo/No.txt"
npart=1e3
cpart=1e2
turns=1E3
zoomturns=1E2
#
set tmargin 3
set title "HL Halo Round"
set yrange[0.65:1]
set xrange[0:turns]
set xlabel "Turn [-]"
set ylabel "N/N_0[-]"
plot (NHR.halo) u 1:($2/npart) title "NH" lt 8, (DCR.halo) u 1:($2/npart) title "DC" lt 2, (ACR.halo) u 1:($2/npart) title "AC" lt 7, (DIFFR.halo) u 1:($2/npart) title "DIFF" lt 4
#
#
unset key
#
set tmargin 3
set title "HL Halo Round Zoom"
set yrange[0.85:1]
set xrange[0:zoomturns]
set xlabel "Turn [-]"
set ylabel "N/N_0[-]"
plot (NHR.halo) u 1:($2/npart) title "NH" lt 8, (DCRhalo) u 1:($2/npart) title "DC" lt 2, (ACR.halo) u 1:($2/npart) title "AC" lt 7, (DIFFR.halo) u 1:($2/npart) title "DIFF" lt 4
#
#
unset key
#
set tmargin 3
set title "HL Round Core"
set yrange[0.99:1.01]
set xrange[0:turns]
set xlabel "Turn [-]"
set ylabel "N/N_0[-]"
plot (NHR.core) u 1:($2/cpart) title "NH" lt 8, (DCR.core) u 1:($2/cpart) title "DC" lt 2, (ACR.core) u 1:($2/cpart) title "AC" lt 7, (DIFFR.core) u 1:($2/cpart) title "DIFF" lt 4
#
#
unset key
#
set tmargin 3
set title "HL NonRound Halo"
set yrange[0.65:1]
set xrange[0:turns]
set xlabel "Turn [-]"
set ylabel "N/N_0[-]"
plot (NHNR.halo) u 1:($2/npart) title "NH" lt 8, (DCNR.halo) u 1:($2/npart) title "DC" lt 2, (ACNR.halo) u 1:($2/npart) title "AC" lt 7, (DIFFNR.halo) u 1:($2/npart) title "DIFF" lt 4
#
#
unset key
#
set tmargin 3
set title "HL Halo NonRound Zoom"
set yrange[0.85:1]
set xrange[0:zoomturns]
set xlabel "Turn [-]"
set ylabel "N/N_0[-]"
plot (NHNR.halo) u 1:($2/npart) title "NH" lt 8, (DCNR.halo) u 1:($2/npart) title "DC" lt 2, (ACNR.halo) u 1:($2/npart) title "AC" lt 7, (DIFFNR.halo) u 1:($2/npart) title "DIFF" lt 4
#
#
unset key
#
set tmargin 3
set title "HL NonRound Core"
set yrange[0.99:1.01]
set xrange[0:turns]
set xlabel "Turn [-]"
set ylabel "N/N_0[-]"
plot (NHNR.core) u 1:($2/cpart) title "NH" lt 8, (DCNR.core) u 1:($2/cpart) title "DC" lt 2, (ACNR.core) u 1:($2/cpart) title "AC" lt 7, (DIFFNR.core) u 1:($2/cpart) title "DIFF" lt 4
#
#
unset key
#
unset multiplot
#

