#
# GNUPLOT script to plot assman test case with reference
#
set terminal png size 1600,2000
set output "TCP_bunch.png"
set multiplot layout 3,2 title "TCP Bunch" font ",14"
#
set tmargin 3
set title "XY"
#
#~ unset key
#
#
#~ set xrange[-1E-3:1E-3]
#~ set yrange[-1E-3:1E-3]
#~ set yrange[-5E-5:5E-5]
set xlabel "x [m]"
set ylabel "y [m]"
plot "TCP_bunch.txt" u 3:5 title "XY"
#
set title "XX'"
#
unset key
#
#
#~ set xrange[0:100]
#~ set yrange[0:0.01]
set xlabel "x [m]"
set ylabel "x' [rad]"
plot "TCP_bunch.txt" u 3:4 title "XX'"
#
set title "YY'"
#
unset key
#
#
#~ set xrange[0:100]
#~ set yrange[0:0.01]
set xlabel "y [m]"
set ylabel "y' [rad]"
plot "TCP_bunch.txt" u 5:6 title "YY'"
#
set title "X'Y'"
#
unset key
#
#
#~ set xrange[0:100]
#~ set yrange[0:0.01]
set xlabel "x' [rad]"
set ylabel "y' [rad]"
plot "TCP_bunch.txt" u 4:6 title "X'Y'"
#
set title "CTDP"
#
unset key
#
#
#~ set xrange[0:100]
#~ set yrange[0:0.01]
set xlabel "ct [m]"
set ylabel "dp [-]"
plot "TCP_bunch.txt" u 7:8 title "CTDP"
#
#
unset key
#
#
unset multiplot
#
