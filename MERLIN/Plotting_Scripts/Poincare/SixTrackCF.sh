################################################################################
# GNUPLOT script to plot XX' XY YY' X'Y' Poincare Sections for SixTrack output #
################################################################################
set terminal png size 1600,1800
set output "ST_Poincare.png"
#
ST_file = "coll_ellipse.dat"
M_file = "../merlin/HEL_bunch.txt"
#
set multiplot layout 2,2 title "Poincare Section" font ",14"
set tmargin 3
set pointsize 0.2

# START PLOT XX'
set title "XX'"
set xlabel "x [m]"
set ylabel "x' [rad]"
plot ST_file u ($3/1000):($5/1000) title "SixTrack", M_file u 3:4 title "MERLIN"
# END PLOT

# START PLOT XY
set title "XY"
set xlabel "x [m]"
set ylabel "y [m]"
plot ST_file u ($3/1000):($4/1000) title "SixTrack", M_file u 3:5 title "MERLIN"
# END PLOT

# START PLOT YY'
set title "YY'"
set xlabel "y [m]"
set ylabel "y' [rad]"
plot ST_file u ($4/1000):($6/1000) title "SixTrack", M_file u 5:6 title "MERLIN"
# END PLOT

# START PLOT X'Y'
set title "X'Y'"
set xlabel "x' [rad]"
set ylabel "y' [rad]"
plot ST_file u ($5/1000):($6/1000) title "SixTrack", M_file u 4:6 title "MERLIN"
#END PLOT

unset multiplot

#'###########################################################################################
# GNUPLOT script to plot XX' XY YY' X'Y' Poincare Sections side by side for SixTrack output #
#############################################################################################
set terminal png size 1600,3600
set output "ST_Poincare_sidebyside.png"
#
ST_file = "coll_ellipse.dat"
M_file = "../merlin/HEL_bunch.txt"
#
set multiplot layout 4,2 title "Poincare Section" font ",14"
set tmargin 3
set pointsize 0.2

# START PLOT
set title "XX'"
set xlabel "x [m]"
set ylabel "x' [rad]"
plot ST_file u ($3/1000):($5/1000) title "SixTrack"
# END PLOT
# START PLOT
set title "XX'"
set xlabel "x [m]"
set ylabel "x' [rad]"
plot M_file u 3:4 title "MERLIN"
# END PLOT

# START PLOT
set title "XY"
set xlabel "x [m]"
set ylabel "y [m]"
plot ST_file u ($3/1000):($4/1000) title "SixTrack"
# END PLOT
# START PLOT
set title "XY"
set xlabel "x [m]"
set ylabel "y [m]"
plot M_file u 3:5 title "MERLIN"
#END PLOT

# START PLOT
set title "YY'"
set xlabel "y [m]"
set ylabel "y' [rad]"
plot ST_file u ($4/1000):($6/1000) title "SixTrack"
# END PLOT
# START PLOT
set title "YY'"
set xlabel "y [m]"
set ylabel "y' [rad]"
plot M_file u 5:6 title "MERLIN"
# END PLOT

# START PLOT
set title "X'Y'"
set xlabel "x' [rad]"
set ylabel "y' [rad]"
plot ST_file u ($5/1000):($6/1000) title "SixTrack"
#END PLOT
# START PLOT
set title "X'Y'"
set xlabel "x' [rad]"
set ylabel "y' [rad]"
plot M_file u 4:6 title "MERLIN"
#END PLOT

unset multiplot

########################################################################
# GNUPLOT script to plot Poincare Section XX' zoom for SixTrack output #
########################################################################
set terminal png size 900,1000
set output "ST_Poincare_zoom.png"

set xlabel "x [m]"
set ylabel "x' [rad]"
set xrange[:0]
set yrange[0:]
plot ST_file u ($3/1000):($5/1000) title "SixTrack", M_file u 3:4 title "MERLIN"
