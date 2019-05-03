# Plots all available plottable data from output.mat as individual files
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio 
import sys
import matplotlib.cm as cm	
from matplotlib.lines import Line2D
import os

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
	
	exists = os.path.isfile(filename)
	if exists:
		f = filename
		p = dict()
		sio.loadmat(f, mdict=p)
		dd[label] = p	
		print '\tadd_input_file::Added output data from ', filename, '\t dictionary key: ', label
	else:
		print '\tadd_input_file::File ', filename, 'not found'		
	
	return dd

# Test add_input_file

# Create dd dictionary
dd = dict()
dd = add_input_file(dd, '../Vertical_Scan/610_SbS/output/output.mat', '8')
dd = add_input_file(dd, './1/output/output.mat', '1')
dd = add_input_file(dd, './2/output/output.mat', '2')
dd = add_input_file(dd, './3/output/output.mat', '3')
dd = add_input_file(dd, './4/output/output.mat', '4')
dd = add_input_file(dd, './5/output/output.mat', '5')
dd = add_input_file(dd, './6/output/output.mat', '6')
dd = add_input_file(dd, './7/output/output.mat', '7')
print 'Final data dictionary keys: ', sorted(dd.keys())

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
		ax1.plot(dd[key]['turn'][0], dd[key]['cumulative_time'][0]/3600, label=key, color=colors[int(key)-1]);
	
	legend_elements2 = [Line2D([0], [0], color=colors[0], lw=4),	Line2D([0], [0], color=colors[1], lw=4), Line2D([0], [0], color=colors[2], lw=4), Line2D([0], [0], color=colors[3], lw=4), Line2D([0], [0], color=colors[4], lw=4),	Line2D([0], [0], color=colors[5], lw=4), Line2D([0], [0], color=colors[6], lw=4), Line2D([0], [0], color=colors[7], lw=4)]
	ax1.legend(legend_elements2, ['1 Node', '2 Nodes', '3 Nodes', '4 Nodes', '5 Nodes', '6 Nodes', '7 Nodes', '8 Nodes'], loc=4, frameon=False, )
			
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
		ax1.plot(dd[key]['turn'][0], dd[key]['turn_duration'][0], label=key, color=colors[int(key)-1]);
	
	legend_elements2 = [Line2D([0], [0], color=colors[0], lw=4),	Line2D([0], [0], color=colors[1], lw=4), Line2D([0], [0], color=colors[2], lw=4), Line2D([0], [0], color=colors[3], lw=4), Line2D([0], [0], color=colors[4], lw=4),	Line2D([0], [0], color=colors[5], lw=4), Line2D([0], [0], color=colors[6], lw=4), Line2D([0], [0], color=colors[7], lw=4)]
	ax1.legend(legend_elements2, ['1 Node', '2 Nodes', '3 Nodes', '4 Nodes', '5 Nodes', '6 Nodes', '7 Nodes', '8 Nodes'], loc=4, frameon=False, )
	
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

main_label = 'MD4224_New_FF_Test'

plot_cumulative_time(dd, main_label)
plot_cumulative_time_grouped(dd, main_label)

plot_turn_duration(dd, main_label)
plot_turn_duration(dd, str(main_label+'_zoom'), 500, 15, 120)

plot_turn_duration_grouped(dd, main_label)
plot_turn_duration_grouped(dd, str(main_label+'_zoom'), 500, 15, 120)

print '\n\n\tFinished Plotting'
