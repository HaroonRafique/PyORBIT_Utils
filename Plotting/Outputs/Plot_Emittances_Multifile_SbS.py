# Plots all available plottable data from output.mat as individual files
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import scipy.io as sio 
import matplotlib.cm as cm

plt.rcParams['figure.figsize'] = [8.0, 4.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.rcParams['font.size'] = 10
plt.rcParams['legend.fontsize'] = 'medium'
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

'''
plot_emittance: Required arguments:
dd: 		dictionary of particle data dictionaries. key = user defined label
filename:	e.g. 'Testing' gives Testing_Emittances.png.
turns:		array of turns to plot at, default is 0,874,2185 which correspond to
			c170, c172, c175 (WS measurement times for MD4224)

Optional arguments:
legend_label:	title for legend
y limits are default unless 'ymin' and 'ymax' arguments are specified.
One may provide a plot title using the 'tit' argument.
'''
def plot_emittance(dd, filename, turns=[0,874,2185], ymin=None, ymax=None, tit = None, legend_label = None):
		
	multiplier = 1./1E-6
	
	# First plot for epsn_x
	fig1 = plt.figure(figsize=(8, 8), facecolor='w', edgecolor='k')
	ax1 = fig1.add_subplot(211)	

	colors = cm.rainbow(np.linspace(0, 1, len(turns)))
	c_it = int(0)	
	
	ax1.set_xlabel(r'Q$_y$ [-]');
	ax1.set_ylabel(r'$\epsilon_x^n$ [mm mrad]')
	ax1.set_title('Emittances');
	
	custom_lines = []
	custom_labels = []
	
	t_it = int(0)
	for t in sorted(turns):
		custom_lines.append(Line2D([0], [0], color=colors[t_it], lw=2))
		custom_labels.append(t)
		t_it = t_it +1		
	
	for t in sorted(turns):	
		for key, value in sorted(dd.iteritems()):	
			ax1.scatter(key, dd[key]['epsn_x'][0][t]*multiplier, color=colors[c_it]);
		c_it = c_it + 1	
			
	if ymin is not None:
		ax1.set_ylim(bottom = ymin)	
	if ymax is not None:
		ax1.set_ylim(top = ymax)
	
	ax1.grid(True);	
	
	if legend_label is not None: 		
		ax1.legend(custom_lines, custom_labels, title=legend_label)
	else:		
		ax1.legend(custom_lines, custom_labels)
	
	# Second plot for epsn_y
	ax2 = fig1.add_subplot(212)	
	
	colors = cm.rainbow(np.linspace(0, 1, len(turns)))
	c_it = int(0)	
	
	ax2.set_xlabel(r'Q$_y$ [-]');
	ax2.set_ylabel(r'$\epsilon_y^n$ [mm mrad]')
	
	for t in sorted(turns):	
		for key, value in sorted(dd.iteritems()):	
			ax2.scatter(key, dd[key]['epsn_y'][0][t]*multiplier, color=colors[c_it]);
		c_it = c_it + 1	
			
	if ymin is not None:
		ax2.set_ylim(bottom = ymin)	
	if ymax is not None:
		ax2.set_ylim(top = ymax)
	
	ax2.grid(True);	
	
	if legend_label is not None: 		
		ax2.legend(custom_lines, custom_labels, title=legend_label)
	else:		
		ax2.legend(custom_lines, custom_labels)
	
	figname = filename + '_Emittances.png'
	fig1.savefig(figname);	
	plt.close()
	
	return;

'''
------------------------------------------------------------------------
						Open files and read data
------------------------------------------------------------------------
'''
	
# Test add_input_file

# Create dd dictionary
dd = dict()
dd = add_input_file(dd, './624_SbS/output/output.mat', 6.24)
dd = add_input_file(dd, './622_SbS/output/output.mat', 6.22)
dd = add_input_file(dd, './620_SbS/output/output.mat', 6.20)
dd = add_input_file(dd, './618_SbS/output/output.mat', 6.18)
dd = add_input_file(dd, './616_SbS/output/output.mat', 6.16)
dd = add_input_file(dd, './614_SbS/output/output.mat', 6.14)
dd = add_input_file(dd, './612_SbS/output/output.mat', 6.12)
dd = add_input_file(dd, './610_SbS/output/output.mat', 6.10)
print 'Final data dictionary keys: ', dd.keys()
		
main_label = 'Slice_By_Slice'
legend_label = 'Tune'
turn_tot = None
turns = [0, 1, 10, 100, 199, 50]

'''
------------------------------------------------------------------------
								Plot
------------------------------------------------------------------------
'''

plot_emittance(dd, main_label, turns, legend_label='Turn')

# ~ plot_parameter(dd, parameter = 'intensity', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
# ~ plot_parameter(dd, parameter = 'intensity', filename = main_label,  percentage = True, turns = turn_tot, legend_label = legend_label)

# ~ plot_parameter(dd, parameter = 'mean_x', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
# ~ plot_parameter(dd, parameter = 'mean_x', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

# ~ plot_parameter(dd, parameter = 'mean_xp', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
# ~ plot_parameter(dd, parameter = 'mean_xp', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

# ~ plot_parameter(dd, parameter = 'mean_y', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
# ~ plot_parameter(dd, parameter = 'mean_y', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

# ~ plot_parameter(dd, parameter = 'mean_yp', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
# ~ plot_parameter(dd, parameter = 'mean_yp', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

# ~ plot_parameter(dd, parameter = 'mean_z', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
# ~ plot_parameter(dd, parameter = 'mean_z', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

# ~ plot_parameter(dd, parameter = 'mean_dE', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
# ~ plot_parameter(dd, parameter = 'mean_dE', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

# ~ plot_parameter(dd, parameter = 'epsn_x', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label, ymin=1, ymax=2.2)
# ~ plot_parameter(dd, parameter = 'epsn_x', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

# ~ plot_parameter(dd, parameter = 'epsn_y', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
# ~ plot_parameter(dd, parameter = 'epsn_y', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

# ~ plot_parameter(dd, parameter = 'eps_z', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
# ~ plot_parameter(dd, parameter = 'eps_z', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

# ~ plot_parameter(dd, parameter = 'bunchlength', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
# ~ plot_parameter(dd, parameter = 'bunchlength', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

# ~ plot_parameter(dd, parameter = 'dpp_rms', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
# ~ plot_parameter(dd, parameter = 'dpp_rms', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

# ~ plot_mean_of_two_parameters(dd, parameter1 = 'epsn_x', parameter2 = 'epsn_y', filename = main_label,  legend_label = legend_label)
