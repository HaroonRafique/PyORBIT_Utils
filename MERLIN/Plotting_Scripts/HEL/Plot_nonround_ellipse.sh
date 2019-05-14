#
# GNUPLOT script to plot non round HEL
#
set terminal png size 800,800
set output "NonRound_noHEL_100turns_4-6sig_HELHalo.png"
#
set xlabel "x [m]"
set ylabel "y [m]"
#
#
set pointsize 5
#
# Set axes limits
set yrange [-0.003:0.003]                     
set xrange [-0.003:0.003]  
#
# ellipse that matches distribution NONROUND
#~ set object 1 ellipse center 0,0 size (8*0.0003944915997),(8*0.0003191784002) angle 0. front fs empty bo -1 lw 3
#
# ellipse that matches distribution ROUND
#~ set object 1 ellipse center 0,0 size (8*0.0003191784002),(8*0.000314734283) angle 0. front fs empty bo -1 lw 3
#
# circle of HEL inner radius 4-8sig NONROUND
set object 2 ellipse center 0,0 size (4*0.0003944915997),(4*0.0003944915997) angle 0. front fs empty bo 7 lw 3
set object 3 ellipse center 0,0 size (8*0.0003944915997),(8*0.0003944915997) angle 0. front fs empty bo 7 lw 3
#
# circle of HEL inner radius 4-8sig ROUND
#~ set object 2 ellipse center 0,0 size (4*0.000314734283),(4*0.000314734283) angle 0. front fs empty bo 7 lw 3
#~ set object 3 ellipse center 0,0 size (8*0.000314734283),(8*0.000314734283) angle 0. front fs empty bo 7 lw 3
#
# suggested HEL elliptical cleaning
#~ set object 3 ellipse center 0,0 size 3.16E-3,3.16E-3 angle 0. front fs empty bo 4 lw 3
#~ set object 3 ellipse center 0,0 size 3.16E-3,3.16E-3 angle 0. front fs empty bo 4 lw 3
#
#
set pointsize 1
#Plot HEL distribution
plot "HEL_bunch.txt" u 3:5 title "HEL"  
