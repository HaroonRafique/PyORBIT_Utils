# Script to open all PTC Twiss (output using 
# pyOrbit_PTCLatticeFunctionsDictionary.py), and plot respective outputs
# over all turns. Useful for seeing things such as the closed orbit bump

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os

plot_CO = True
plot_beta = True
plot_alpha = False
plot_dispersion = False

# Function to open file and create data
# Returns a list where each row is one line of the input file (13 rows)
def ReadTwissReturnData(filename):
	# s	beta_x	beta_y	alpha_x	alpha_y	D_x	D_y	D_px	D_py	orbit_x	orbit_px	orbit_y	orbit_py
	data=dict()
	
	# Open file and skip header
	fin1=open(filename,'r').readlines()[1:]
	
	s=[]		#0
	beta_x=[]	#1
	beta_y=[]	#2
	alpha_x=[]	#3
	alpha_y=[]	#4
	D_x=[]		#5
	D_y=[]		#6
	D_px=[]		#7
	D_py=[]		#8
	orbit_x=[]	#9
	orbit_px=[]	#10
	orbit_y=[]	#11
	orbit_py=[]	#12
	
	for l in fin1:
		s.append(float(l.split()[0]))
		beta_x.append(float(l.split()[1]))
		beta_y.append(float(l.split()[2]))
		alpha_x.append(float(l.split()[3]))
		alpha_y.append(float(l.split()[4]))
		D_x.append(float(l.split()[5]))
		D_y.append(float(l.split()[6]))
		D_px.append(float(l.split()[7]))
		D_py.append(float(l.split()[8]))
		orbit_x.append(float(l.split()[9]))
		orbit_px.append(float(l.split()[10]))
		orbit_y.append(float(l.split()[11]))
		orbit_py.append(float(l.split()[12]))
		
	data = zip(s,beta_x,beta_y,alpha_x,alpha_y,D_x,D_y,D_px,D_py,orbit_x,orbit_px,orbit_y,orbit_py)
	
	return data
	
def ReadAndPlot(filein, ax, index, colors):
	fin1=open(filein,'r').readlines()[1:]
	c_it = int(filein[-5])
	for l in fin1: ax.scatter(float(l.split()[0]), float(l.split()[index]), color=colors[c_it]);

# Create a list of all input files
list_of_files =[]
for file in os.listdir("."):
    if file.endswith(".dat"):
        print 'Found file:', (os.path.join(".", file))
        list_of_files.append(file)
        
# Sort list by turn
sorted_list_of_files = sorted(list_of_files)

# Different colour for each turn (file)
colors = cm.rainbow(np.linspace(0, 1, len(sorted_list_of_files)+1))
# ~ c_it = int(0)

# Open all figures
fig_h_size = 14
fig_v_size = 9


if plot_beta:
	fig1 = plt.figure(1, figsize=(fig_h_size, fig_v_size), facecolor='w', edgecolor='k')
	ax1 = fig1.add_subplot(111)
	ax1.set_xlabel('s [m]');
	ax1.set_ylabel(r'$\beta_x$ [m]')
	tit1 = r'$\beta_x$'
	ax1.set_title(tit1);
	ax1.grid()

	fig2 = plt.figure(2, figsize=(fig_h_size, fig_v_size), facecolor='w', edgecolor='k')
	ax2 = fig2.add_subplot(111)
	ax2.set_xlabel('s [m]');
	ax2.set_ylabel(r'$\beta_y$ [m]')
	tit2 = r'$\beta_y$'
	ax2.set_title(tit2);
	ax2.grid()

if plot_CO:

	fig3 = plt.figure(3, figsize=(fig_h_size, fig_v_size), facecolor='w', edgecolor='k')
	ax3 = fig3.add_subplot(111)
	ax3.set_xlabel('s [m]');
	ax3.set_ylabel(r'CO$_x$ [m]')
	tit3 = 'Horizontal Closed Orbit'
	ax3.set_title(tit3);
	ax3.grid()

	fig4 = plt.figure(4, figsize=(fig_h_size, fig_v_size), facecolor='w', edgecolor='k')
	ax4 = fig4.add_subplot(111)
	ax4.set_xlabel('s [m]');
	ax4.set_ylabel(r'CO$_y$ [m]')
	tit4 = 'Vertical Closed Orbit'
	ax4.set_title(tit4);
	ax4.grid()

# Iterate through files by turn, open file, read data
for f in sorted_list_of_files:
	print 'Plotting turn ', f[-5]
	if plot_CO: 
		ReadAndPlot(f, ax3, 9, colors)
		ReadAndPlot(f, ax4, 11, colors)	
	if plot_beta: 
		ReadAndPlot(f, ax1, 1, colors)
		ReadAndPlot(f, ax2, 2, colors)
		
# Old method
# ~ turn_dat = ReadTwissReturnData(f)
# Add to plot
	# ~ for i in xrange(len(turn_dat)):
		# ~ if plot_beta: 
			# ~ ax1.scatter(turn_dat[i][0], turn_dat[i][1], color=colors[c_it]);
			# ~ ax2.scatter(turn_dat[i][0], turn_dat[i][2], color=colors[c_it]);
		# ~ if plot_CO:
			# ~ ax3.scatter(turn_dat[i][0], turn_dat[i][9], color=colors[c_it]);
			# ~ ax4.scatter(turn_dat[i][0], turn_dat[i][11], color=colors[c_it]);
		
	# ~ c_it += 1

if plot_beta:
	figname1 = 'beta_x.png'
	fig1.savefig(figname1);

	figname2 = 'beta_y.png'
	fig2.savefig(figname2);

if plot_CO:
	figname3 = 'orbit_x.png'
	fig3.savefig(figname3);

	figname4 = 'orbit_y.png'
	fig4.savefig(figname4);






























