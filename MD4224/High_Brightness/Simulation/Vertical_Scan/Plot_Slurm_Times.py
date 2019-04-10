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
dd = add_input_file(dd, './610_SbS/output/output.mat', '10_SbS N=1 HT=1')
dd = add_input_file(dd, './612_SbS/output/output.mat', '12_SbS N=1 HT=0')
dd = add_input_file(dd, './614_SbS/output/output.mat', '14_SbS N=2 HT=1')
dd = add_input_file(dd, './616_SbS/output/output.mat', '16_SbS N=2 HT=0')
dd = add_input_file(dd, './618_SbS/output/output.mat', '18_SbS N=3 HT=1')
dd = add_input_file(dd, './620_SbS/output/output.mat', '20_SbS N=3 HT=0')
dd = add_input_file(dd, './622_SbS/output/output.mat', '22_SbS N=4 HT=1')
dd = add_input_file(dd, './624_SbS/output/output.mat', '24_SbS N=4 HT=0')
dd = add_input_file(dd, './610_2p5/output/output.mat', '10_2.5 N=1 HT=1')
dd = add_input_file(dd, './612_2p5/output/output.mat', '12_2.5 N=1 HT=0')
dd = add_input_file(dd, './614_2p5/output/output.mat', '14_2.5 N=2 HT=1')
dd = add_input_file(dd, './616_2p5/output/output.mat', '16_2.5 N=2 HT=0')
dd = add_input_file(dd, './618_2p5/output/output.mat', '18_2.5 N=3 HT=1')
dd = add_input_file(dd, './620_2p5/output/output.mat', '20_2.5 N=3 HT=0')
dd = add_input_file(dd, './622_2p5/output/output.mat', '22_2.5 N=4 HT=1')
dd = add_input_file(dd, './624_2p5/output/output.mat', '24_2.5 N=4 HT=0')
print 'Final data dictionary keys: ', dd.keys()

'''
plot_cumulative_time
dd: dictionary of particle data dictionaries. key = user defined label
ml: main label for plot file name

'''
def plot_cumulative_time_grouped(dd, ml):
	
	fig1 = plt.figure(facecolor='w', edgecolor='k')
	ax1 = fig1.add_subplot(111)
	
	num_N = 8
	
	colors = cm.rainbow(np.linspace(0, 1, num_N))
	
	for key, value in sorted(dd.iteritems()):		
		if 'N=1' in key:
			if 'HT=0' in key:
				col = colors[0]
			elif 'HT=1' in key:
				col = colors[1]
		elif 'N=2' in key:
			if 'HT=0' in key:
				col = colors[2]
			elif 'HT=1' in key:
				col = colors[3]
		elif 'N=3' in key:
			if 'HT=0' in key:
				col = colors[4]
			elif 'HT=1' in key:
				col = colors[5]
		elif 'N=4' in key:
			if 'HT=0' in key:
				col = colors[6]
			elif 'HT=1' in key:
				col = colors[7]
		else:
			col = 'k'	
		
		ax1.plot(dd[key]['turn'][0], dd[key]['cumulative_time'][0]/3600, label=key, color=col);
	
	legend_elements2 = [Line2D([0], [0], color=colors[0], lw=4, label='1 Node hyperthreading OFF'),	Line2D([0], [0], color=colors[1], lw=4, label='1 Node hyperthreading ON'), Line2D([0], [0], color=colors[2], lw=4, label='2 Nodes hyperthreading OFF'), Line2D([0], [0], color=colors[3], lw=4, label='2 Node hyperthreading ON'), Line2D([0], [0], color=colors[4], lw=4, label='3 Nodes hyperthreading OFF'),	Line2D([0], [0], color=colors[5], lw=4, label='3 Node hyperthreading ON'), Line2D([0], [0], color=colors[6], lw=4, label='4 Nodes hyperthreading OFF'), Line2D([0], [0], color=colors[7], lw=4, label='4 Nodes hyperthreading ON')]
	ax1.legend(legend_elements2, ['1 Node hyperthreading OFF', '1 Node hyperthreading ON', '2 Nodes hyperthreading OFF', '2 Nodes hyperthreading ON', '3 Nodes hyperthreading OFF', '3 Nodes hyperthreading ON', '4 Nodes hyperthreading OFF', '4 Nodes hyperthreading ON'], loc=4, frameon=False, )
			
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
	
	for key, value in sorted(dd.iteritems()):		
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
			
	num_N = 8
	
	colors = cm.rainbow(np.linspace(0, 1, num_N))
	
	for key, value in sorted(dd.iteritems()):
		
		if 'N=1' in key:
			if 'HT=0' in key:
				col = colors[0]
			elif 'HT=1' in key:
				col = colors[1]
		elif 'N=2' in key:
			if 'HT=0' in key:
				col = colors[2]
			elif 'HT=1' in key:
				col = colors[3]
		elif 'N=3' in key:
			if 'HT=0' in key:
				col = colors[4]
			elif 'HT=1' in key:
				col = colors[5]
		elif 'N=4' in key:
			if 'HT=0' in key:
				col = colors[6]
			elif 'HT=1' in key:
				col = colors[7]
		else:
			col = 'k'	
		
		ax1.plot(dd[key]['turn'][0], dd[key]['turn_duration'][0], label=key, color=col);
	
	legend_elements2 = [Line2D([0], [0], color=colors[0], lw=4, label='1 Node hyperthreading OFF'),	Line2D([0], [0], color=colors[1], lw=4, label='1 Node hyperthreading ON'), Line2D([0], [0], color=colors[2], lw=4, label='2 Nodes hyperthreading OFF'), Line2D([0], [0], color=colors[3], lw=4, label='2 Node hyperthreading ON'), Line2D([0], [0], color=colors[4], lw=4, label='3 Nodes hyperthreading OFF'),	Line2D([0], [0], color=colors[5], lw=4, label='3 Node hyperthreading ON'), Line2D([0], [0], color=colors[6], lw=4, label='4 Nodes hyperthreading OFF'), Line2D([0], [0], color=colors[7], lw=4, label='4 Nodes hyperthreading ON')]
	ax1.legend(legend_elements2, ['1 Node hyperthreading OFF', '1 Node hyperthreading ON', '2 Nodes hyperthreading OFF', '2 Nodes hyperthreading ON', '3 Nodes hyperthreading OFF', '3 Nodes hyperthreading ON', '4 Nodes hyperthreading OFF', '4 Nodes hyperthreading ON'], loc=4, frameon=False, )
	
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
	
	for key, value in sorted(dd.iteritems()):
		
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

main_label = 'PyORBIT_HPC-Batch_2p5D_vs_SBS'

plot_cumulative_time(dd, main_label)
plot_cumulative_time_grouped(dd, main_label)

plot_turn_duration(dd, main_label)
plot_turn_duration(dd, str(main_label+'_zoom'), 500, 15, 120)

plot_turn_duration_grouped(dd, main_label)
plot_turn_duration_grouped(dd, str(main_label+'_zoom'), 500, 15, 120)

print '\n\n\tFinished Plotting'
