# Plots all available plottable data from output.mat as individual files
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio 
import sys
import matplotlib.cm as cm	
from matplotlib.lines import Line2D

plt.rcParams['figure.figsize'] = [8.0, 4.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.rcParams['font.size'] = 10
plt.rcParams['legend.fontsize'] = 'small'
plt.rcParams['lines.linewidth'] = 1

'''
add_input_file:
dd: dictionary of particle data dictionaries. key = user defined label
filename: input file name (with relative path from this file)
label: file label e.g. 'case 1', 'case 2', ...
'''
def add_input_file(dd, filename, label):
	f = filename
	p = dict()
	sio.loadmat(f, mdict=p)
	dd[label] = p	
	print '\n\tAdded output data from ', filename, '\t dictionary key: ', label
	return dd

# Test add_input_file

# Create dd dictionary
dd = dict()
dd = add_input_file(dd, './Horizontal_Scan/21/output/output.mat', '21 N=2 HT=0')
dd = add_input_file(dd, './Horizontal_Scan/19/output/output.mat', '19 N=2 HT=1')
dd = add_input_file(dd, './Horizontal_Scan/17/output/output.mat', '17 N=2 HT=0')
dd = add_input_file(dd, './Horizontal_Scan/15/output/output.mat', '15 N=2 HT=1')
dd = add_input_file(dd, './Horizontal_Scan/13/output/output.mat', '13 N=1 HT=0')
dd = add_input_file(dd, './Horizontal_Scan/11/output/output.mat', '11 N=1 HT=1')
dd = add_input_file(dd, './Horizontal_Scan/09/output/output.mat', '09 N=1 HT=0')
dd = add_input_file(dd, './Horizontal_Scan/07/output/output.mat', '07 N=1 HT=1')
dd = add_input_file(dd, './Horizontal_Scan/09/output/output.mat', '24 N=2 HT=0')
dd = add_input_file(dd, './Horizontal_Scan/09/output/output.mat', '22 N=2 HT=1')
dd = add_input_file(dd, './Horizontal_Scan/09/output/output.mat', '20 N=2 HT=0')
dd = add_input_file(dd, './Horizontal_Scan/09/output/output.mat', '18 N=2 HT=1')
dd = add_input_file(dd, './Horizontal_Scan/09/output/output.mat', '16 N=1 HT=0')
dd = add_input_file(dd, './Horizontal_Scan/09/output/output.mat', '14 N=1 HT=1')
dd = add_input_file(dd, './Horizontal_Scan/09/output/output.mat', '12 N=1 HT=0')
dd = add_input_file(dd, './Horizontal_Scan/07/output/output.mat', '10 N=1 HT=1')
print 'Final data dictionary keys: ', dd.keys()

'''
plot_cumulative_time
dd: dictionary of particle data dictionaries. key = user defined label
ml: main label for plot file name

'''
def plot_cumulative_time_grouped(dd, ml):
	
	fig1 = plt.figure(facecolor='w', edgecolor='k')
	ax1 = fig1.add_subplot(111)
	
	for key, value in dd.iteritems():
		
		if 'N=1' in key:
			if 'HT=0' in key:
				col = 'r'
			elif 'HT=1' in key:
				col = 'orange'
		elif 'N=2' in key:
			if 'HT=0' in key:
				col = 'b'
			elif 'HT=1' in key:
				col = 'g'
		else:
			col = 'k'	
		
		ax1.plot(dd[key]['turn'][0], dd[key]['cumulative_time'][0]/3600, label=key, color=col);
	
	legend_elements2 = [Line2D([0], [0], color='r', lw=4, label='1 Node hyperthreading OFF'), Line2D([0], [0], color='orange', lw=4, label='1 Node hyperthreading ON'), Line2D([0], [0], color='b', lw=4, label='2 Nodes hyperthreading OFF'), Line2D([0], [0], color='g', lw=4, label='2 Nodes hyperthreading ON')]
	ax1.legend(legend_elements2, ['1 Node hyperthreading OFF', '1 Node hyperthreading ON', '2 Nodes hyperthreading OFF', '2 Nodes hyperthreading ON'], loc=4, frameon=False, )
			
	# ~ ax1.legend(frameon=False, loc=4)
	ax1.set_xlabel('Turn [-]');
	ax1.set_ylabel('Time [hours]')
	ax1.set_title('Grouped Cumulative Time');
	ax1.grid(True);
	

	
	figname = ml + '_cumulative_time_grouped.png'
	
	fig1.savefig(figname);	
	
	return
	
def plot_cumulative_time(dd, ml):
	
	fig1 = plt.figure(facecolor='w', edgecolor='k')
	ax1 = fig1.add_subplot(111)	
	
	colors = cm.rainbow(np.linspace(0, 1, len(dd.keys())))
	c_it = int(0)
	
	for key, value in dd.iteritems():		
		ax1.plot(dd[key]['turn'][0], dd[key]['cumulative_time'][0]/3600, label=key, color=colors[c_it]);
		c_it = c_it + 1
		
	ax1.legend(frameon=False, loc=4)
	ax1.set_xlabel('Turn [-]');
	ax1.set_ylabel('Time [hours]')
	ax1.set_title('Cumulative Time');
	ax1.grid(True);
	
	figname = ml + '_cumulative_time.png'
	
	fig1.savefig(figname);	
	
	return


def plot_turn_duration_grouped(dd, ml, turns=None, ymin=None, ymax=None):
	
	fig1 = plt.figure(facecolor='w', edgecolor='k')
	ax1 = fig1.add_subplot(111)
	
	for key, value in dd.iteritems():
		
		if 'N=1' in key:
			if 'HT=0' in key:
				col = 'r'
			elif 'HT=1' in key:
				col = 'orange'
		elif 'N=2' in key:
			if 'HT=0' in key:
				col = 'b'
			elif 'HT=1' in key:
				col = 'g'
		else:
			col = 'k'	
		
		ax1.plot(dd[key]['turn'][0], dd[key]['turn_duration'][0], label=key, color=col);
	
	legend_elements2 = [Line2D([0], [0], color='r', lw=4, label='1 Node hyperthreading OFF'), Line2D([0], [0], color='orange', lw=4, label='1 Node hyperthreading ON'), Line2D([0], [0], color='b', lw=4, label='2 Nodes hyperthreading OFF'), Line2D([0], [0], color='g', lw=4, label='2 Nodes hyperthreading ON')]
	ax1.legend(legend_elements2, ['1 Node hyperthreading OFF', '1 Node hyperthreading ON', '2 Nodes hyperthreading OFF', '2 Nodes hyperthreading ON'], loc=2, frameon=False, )

	# ~ ax1.legend(frameon=False, loc=4)
	ax1.set_xlabel('Turn [-]');
	ax1.set_ylabel('Time [seconds]')
	ax1.set_title('Grouped Time for 1 Simulation Turn');
	ax1.grid(True);
	
	if turns is not None: 
		ax1.set_xlim(left = 0)
		ax1.set_xlim(right = turns)
	if ymin is not None:
		ax1.set_ylim(bottom = ymin)	
	if ymax is not None:
		ax1.set_ylim(top = ymax)
	
	figname = ml + '_turn_duration_grouped.png'
	fig1.savefig(figname);	
	
	return


def plot_turn_duration(dd, ml, turns=None, ymin=None, ymax=None):
	
	fig1 = plt.figure(facecolor='w', edgecolor='k')
	ax1 = fig1.add_subplot(111)	
	
	colors = cm.rainbow(np.linspace(0, 1, len(dd.keys())))
	c_it = int(0)
	
	for key, value in dd.iteritems():
		
		ax1.plot(dd[key]['turn'][0], dd[key]['turn_duration'][0], label=key, color=colors[c_it]);		
		c_it = c_it + 1
		
	ax1.legend(frameon=False, loc=4)
	ax1.set_xlabel('Turn [-]');
	ax1.set_ylabel('Time [seconds]')
	ax1.set_title('Time for 1 Simulation Turn');
	ax1.grid(True);
	
	if turns is not None: 
		ax1.set_xlim(left = 0)
		ax1.set_xlim(right = turns)
	if ymin is not None:
		ax1.set_ylim(bottom = ymin)	
	if ymax is not None:
		ax1.set_ylim(top = ymax)
	
	figname = ml + '_turn_duration.png'
	fig1.savefig(figname);	
	
	return

main_label = 'PyORBIT_HPC-Batch'

plot_cumulative_time(dd, main_label)
plot_cumulative_time_grouped(dd, main_label)

plot_turn_duration(dd, main_label)
plot_turn_duration(dd, str(main_label+'_zoom'), 500, 15, 120)

plot_turn_duration_grouped(dd, main_label)
plot_turn_duration_grouped(dd, str(main_label+'_zoom'), 500, 15, 120)

print '\n\n\tFinished Plotting'
