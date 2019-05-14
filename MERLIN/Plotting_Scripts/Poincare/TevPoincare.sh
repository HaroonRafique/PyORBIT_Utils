#
# GNUPLOT script to plot phase ellipse
#
set terminal png size 800,1000
set output "TevatronHEL.png"
#~ set tmargin 2
#
set pointsize 0.2
#
set xlabel "x [m]"
set ylabel "x' [rad]"
#
#
set xrange[:0]
set yrange[0:]
#~ plot "total_bunch.txt" u 3:4 title "DC TRANSPORT + HELProcess no_RF"
#~ plot "total_bunch.txt" u 3:4 title "DC TRANSPORT + SymplecticHELProcess"
plot "total_bunch.txt" u 3:4 title ""
#~ plot "total_bunch.txt" u 3:4 title "DC SYMPLECTIC + HELProcess"
#
#
#~ unset key
#
#
#~ set xrange[0:100]
#~ set yrange[0:0.01]
#~ plot "total_bunch.txt" u ($3*1000):($4*1000) title "DC HL v1.2.1 TTDistn 1-10sig @ IP1"
#
#plot "Ref.dat" u 1:2 title "reference", "HEL_S_hist.txt" u 1:2 title "merged" 
#
#
#~ unset multiplot
