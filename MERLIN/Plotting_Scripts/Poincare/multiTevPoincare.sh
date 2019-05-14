#
# GNUPLOT script to plot phase ellipse
#
set terminal png size 1600,2000
set output "Poincare.png"
#
set multiplot layout 3,2 title "Poincare Section" font ",14"
#
set tmargin 3
#
set pointsize 0.2
# Tev HEL Sigma
#  0.0002919978486
#
# START PLOT
#
set title "XX'"
#
set xlabel "x [m]"
set ylabel "x' [rad]"
#
#~ set xrange[:0]
#~ set yrange[0:]
#
f(y) = 0.001
plot "HEL_bunch.txt" u 3:4 title "",f(y)
#~ plot (4*0.0002919978486)
#~ set arrow 1 from (4*0.0002919978486),1 to (4*0.0002919978486),-1 style arrow 7 nohead ls 1
#~ set arrow 1 from (0.001),1 to (0.001),-1 style arrow 7 nohead ls 1

#
#END PLOT
#
# START PLOT
#
set title "XY"
#
set xlabel "x [m]"
set ylabel "y [m]"
#
#~ set xrange[:]
#~ set yrange[:]
#
plot "HEL_bunch.txt" u 3:5 title ""
#
#END PLOT
## START PLOT
#
set title "YY'"
#
set xlabel "y [m]"
set ylabel "y' [rad]"
#
#~ set xrange[:]
#~ set yrange[:]
#
plot "HEL_bunch.txt" u 5:6 title ""
#
#END PLOT
#
# START PLOT
#
set title "X'Y'"
#
set xlabel "x' [rad]"
set ylabel "y' [rad]"
#
#~ set xrange[:]
#~ set yrange[:]
#
plot "HEL_bunch.txt" u 4:6 title ""
#
#END PLOT
#
# START PLOT
#
set title "CTDP"
#
set xlabel "ct [m]"
set ylabel "dp [-]"
#
#~ set xrange[:]
#~ set yrange[:]
#
plot "HEL_bunch.txt" u 7:8 title ""
#
#END PLOT
#

#
unset multiplot
