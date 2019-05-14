#
# GNUPLOT script to plot HEL footprint - assumes initial injection @ HEL
#
set terminal png size 900,800
set output "HEL_footprint.png"
#
set tmargin 3
set title "XY"
#
#~ unset key
#
#
set xrange[-3E-3:3E-3]
set yrange[-3E-3:3E-3]
# circle of HEL inner radius 4-6.8sig ROUND LHC
#~ set object 2 ellipse center 0,0 size (2*0.001167991394),(2*0.001167991394) angle 0. front fs empty bo 7 lw 3
#~ set object 3 ellipse center 0,0 size (2*0.00198558537),(2*0.00198558537) angle 0. front fs empty bo 7 lw 3
# circle of HEL inner radius 4-8sig NONROUND HL
#~ set object 2 ellipse center 0,0 size (2*0.00157793977),(2*0.00157793977) angle 0. front fs empty bo 7 lw 3
#~ set object 3 ellipse center 0,0 size (2*0.003155879539),(2*0.003155879539) angle 0. front fs empty bo 7 lw 3
# circle of HEL inner radius 4-8sig ROUND HL
#~ set object 2 ellipse center 0,0 size (2*0.001258945051),(2*0.001258945051) angle 0. front fs empty bo 7 lw 3
#~ set object 3 ellipse center 0,0 size (2*0.002517890103),(2*0.002517890103) angle 0. front fs empty bo 7 lw 3
#
set xlabel "x [m]"
set ylabel "y [m]"
plot "HEL_bunch.txt" u 3:5 title "100 turns", "initial_bunch.txt" u 3:5 title "initial turn"
#
#
