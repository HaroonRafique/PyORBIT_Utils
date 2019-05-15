#
# GNUPLOT script to plot HEL profiles
#
set terminal png size 600,1000
set output "HEL_Profile.png"
#~ set tmargin 2
set multiplot layout 2,1 
#
set pointsize 0.5
#
set xlabel "R [sigma]"
set ylabel "kick [nrad]"
#
#
#~ set xrange[:0]
#~ set yrange[0:]
plot "profile.txt" u 1:($2/1E-9) title "Radial", "profile.txt" u 1:($3/1E-9) title "Simple"
#
set xlabel "R [sigma]"
set ylabel "|kick| [nrad]"
plot "profile.txt" u 1:($4/1E-9) title "Radial", "profile.txt" u 1:($5/1E-9) title "Simple"
