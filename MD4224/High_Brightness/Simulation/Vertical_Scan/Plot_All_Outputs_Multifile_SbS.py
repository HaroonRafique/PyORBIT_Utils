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
			try:
				ax1.scatter(key, dd[key]['epsn_x'][0][t]*multiplier, color=colors[c_it]);
			except IndexError:
				print 'plot_emittance: index ', t , ' out of range for tune ', key
				continue
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
			try:
				ax2.scatter(key, dd[key]['epsn_y'][0][t]*multiplier, color=colors[c_it]);
			except IndexError:
				# ~ print 'plot_emittance: index ', t , ' out of range for tune ', key
				continue
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
plot_parameter: Required arguments:
dd: dictionary of particle data dictionaries. key = user defined label
parameter name: e.g. 'bunchlength'.
filename: 		e.g. 'Testing' gives Testing_bunchlength.png.

Optional arguments:
percentage:		switch used to plot raw or percentage change from initial value.
legend_label:	title for legend
y limits are default unless 'ymin' and 'ymax' arguments are specified.
x limits may be changed with 'turns' argument.

If the parameter is not an expected one (i.e. from the list below):

	The y-axis label will be 'ylab' + 'yun' arguments
	For example if ylab = 'distance' and yun '[m]' => 'distance [m]'.

	One may specify a parameter multiplier using the 'multi' argument. 
	For example if 'multi' = 1./1E-3, a distance will change from [m] to
	[mm].
	
	One may provide a plot title using the 'tit' argument.

Expected parameters (from PyORBIT script):
------------------------------------------------------------------------
output.addParameter('turn', lambda: turn)
output.addParameter('intensity', lambda: bunchtwissanalysis.getGlobalMacrosize())
output.addParameter('n_mp', lambda: bunchtwissanalysis.getGlobalCount())
output.addParameter('gamma', lambda: bunch.getSyncParticle().gamma())
output.addParameter('mean_x', lambda: bunchtwissanalysis.getAverage(0))
output.addParameter('mean_xp', lambda: bunchtwissanalysis.getAverage(1))
output.addParameter('mean_y', lambda: bunchtwissanalysis.getAverage(2))
output.addParameter('mean_yp', lambda: bunchtwissanalysis.getAverage(3))
output.addParameter('mean_z', lambda: bunchtwissanalysis.getAverage(4))
output.addParameter('mean_dE', lambda: bunchtwissanalysis.getAverage(5))
output.addParameter('epsn_x', lambda: bunchtwissanalysis.getEmittanceNormalized(0))
output.addParameter('epsn_y', lambda: bunchtwissanalysis.getEmittanceNormalized(1))
output.addParameter('eps_z', lambda: get_eps_z(bunch, bunchtwissanalysis))
output.addParameter('bunchlength', lambda: get_bunch_length(bunch, bunchtwissanalysis))
output.addParameter('dpp_rms', lambda: get_dpp(bunch, bunchtwissanalysis))
------------------------------------------------------------------------
'''
def plot_parameter(dd, parameter, filename, percentage = False, ymin=None, ymax=None, ylab=None, yun = None, tit = None, multi=None, turns = None, legend_label = None):
	
	if percentage:
		print '\nPlotting ', parameter, ' percentage'
	else:
		print '\nPlotting ', parameter
	
	multiplier = 1.

	fig1 = plt.figure(facecolor='w', edgecolor='k')
	ax1 = fig1.add_subplot(111)
	
	if parameter is 'bunchlength':
		multiplier = 1./1E-9
		ylabel = r'$B_l$' 
		yunit = '[ns]'
		ax1.set_title('Bunch Length');
		figname = filename + '_' + parameter
		
	elif parameter is 'dpp_rms':
		multiplier = 1./1E-3
		ylabel = r'$\frac{\delta p}{p}$'
		yunit = '[MeV]'
		ax1.set_title(r'$\frac{\delta p}{p}$');		
		figname = filename + '_dpp_rms'
		
	elif parameter is 'mean_x':
		multiplier = 1./1E-3
		ylabel = '<x>' 
		yunit = '[mm]'
		ax1.set_title('Mean x');
		figname = filename + '_' + parameter
	
	elif parameter is 'mean_y':
		multiplier = 1./1E-3
		ylabel = '<y>' 
		yunit = '[mm]'
		ax1.set_title('Mean y');
		figname = filename + '_' + parameter
	
	elif parameter is 'mean_xp':
		multiplier = 1./1E-3
		ylabel = '<x\'>' 
		yunit = '[mrad]'
		ax1.set_title('Mean x\'');
		figname = filename + '_' + parameter
	
	elif parameter is 'mean_yp':
		multiplier = 1./1E-3
		ylabel = '<y\'>' 
		yunit = '[mrad]'
		ax1.set_title('Mean y\'');
		figname = filename + '_' + parameter
		
	elif parameter is 'mean_z':
		ylabel = '<z>'
		yunit = '[m]'
		ax1.set_title('Mean z');
		figname = filename + '_' + parameter
	
	elif parameter is 'mean_dE':
		multiplier = 1./1E-3
		ylabel = '<dE>'
		yunit = '[MeV]'
		ax1.set_title('Mean dE');
		figname = filename + '_' + parameter
							
	elif parameter is 'intensity':
		ylabel = 'I'
		yunit = '[protons]'
		ax1.set_title('Intensity');
		figname = filename + '_' + parameter
	
	elif parameter is 'epsn_x':
		multiplier = 1./1E-6
		ylabel = r'$\epsilon_x^n$'
		yunit = '[mm mrad]'
		ax1.set_title('Horizontal Emittance');
		figname = filename + '_' + parameter
		
	elif parameter is 'epsn_y':
		multiplier = 1./1E-6
		ylabel = r'$\epsilon_y^n$'
		yunit = '[mm mrad]'
		ax1.set_title('Vertical Emittance');
		figname = filename + '_' + parameter
	
	elif parameter is 'eps_z':
		ylabel = r'$\epsilon_z$'
		yunit = '[eV s]'
		ax1.set_title('Longitudinal Emittance');
		figname = filename + '_' + parameter

	else:
		multiplier = multi
		ylabel = ylab
		yunit = yun
		ax1.set_title(tit);
		figname = filename + '_' + parameter


	colors = cm.rainbow(np.linspace(0, 1, len(dd.keys())))
	c_it = int(0)	
	
	if percentage:	
		for key, value in sorted(dd.iteritems()):
			ax1.plot(dd[key]['turn'][0], ((dd[key][parameter][0]/dd[key][parameter][0][0])*100)-100, label=key, color=colors[c_it]);
			c_it = c_it + 1
		ylabel = str(ylabel + ' percentage change [%]')		
		figname = filename + '_' + parameter + '_percentage'
	else:
		for key, value in sorted(dd.iteritems()):			
			ax1.plot(dd[key]['turn'][0], dd[key][parameter][0]*multiplier, label=key, color=colors[c_it]);
			c_it = c_it + 1
		ylabel = str(ylabel + ' ' + yunit)
		
	if ymin is not None:
		ax1.set_ylim(bottom = ymin)	
	if ymax is not None:
		ax1.set_ylim(top = ymax)
		
	if turns is not None: 
		ax1.set_xlim(left = 0)
		ax1.set_xlim(right = turns)
	
	ax1.set_ylabel(ylabel);
	ax1.set_xlabel('Turn [-]');
	ax1.grid(True);
	
	figname = figname + '.png'
	
	if legend_label is not None: 
		ax1.legend(title=legend_label)
	else:
		ax1.legend()
		
	fig1.savefig(figname);	
	plt.close()
	return;

'''
plot_mean_of_two_parameters: Required arguments:
dd: dictionary of particle data dictionaries. key = user defined label
parameter1 name: 	e.g. 'epsn_x'.
parameter1 name: 	e.g. 'epsn_y'.
filename: 			e.g. 'Testing' gives Testing_bunchlength.png.
Optional arguments:
tit:				plot title
ylab:				y-axis label
yun:				y-axis unit
legend_label:		title for legend
y limits are default unless 'ymin' and 'ymax' arguments are specified.
x limits may be changed with 'turns' argument.

The only expected parameters are epsn_x and epsn_y
'''
def plot_mean_of_two_parameters(dd, parameter1, parameter2, filename, tit=None, ylab=None, yun='-', ymin=None, ymax=None, turns = None, legend_label = None):

	print '\nPlotting mean of ', parameter1, 'and', parameter2,
		
	fig1 = plt.figure(figsize=(6,4))
	ax1 = fig1.add_subplot(111)
	
			
	if ylab is None:
		ylab = 'mean of ' + parameter1 + ' and ' + parameter2
		
	if tit is None:
		tit = 'mean of ' + parameter1 + ' and ' + parameter2
				
	colors = cm.rainbow(np.linspace(0, 1, len(dd.keys())))
	c_it = int(0)	
		
	if parameter1 is parameter2:
		print '\nWARNING: plot_mean_of_two_parameters has been given the same parameter ' + parameter1 + ' twice'
		
	if 'epsn' in parameter1 and parameter2:
		multiplier = 1./1E-6
		tit = r'$\left(\frac{\epsilon_x^n + \epsilon_y^n}{2}\right)$'
		ylabel = r'$\left(\frac{\epsilon_x^n + \epsilon_y^n}{2}\right)$'
		yun = '[mm mrad]'		
		
		for key, value in sorted(dd.iteritems()):		
			ax1.plot(dd[key]['turn'][0], (dd[key][parameter1][0]*multiplier + dd[key][parameter2][0]*multiplier)/2, label=key, color=colors[c_it]);
			c_it = c_it + 1
	
		ylabel = ylabel + ' ' + yun
		ax1.set_ylabel(ylabel);
		figname = filename + '_mean_of_' + parameter1 + '_' + parameter2 + '_nodes.png'
	else:
		for key, value in sorted(dd.iteritems()):		
			ax1.plot(dd[key]['turn'][0], (dd[key][parameter1][0]*multiplier + dd[key][parameter2][0]*multiplier)/2, label=key, color=colors[c_it]);
			c_it = c_it + 1
	
		ylabel = str( 'mean of ' + parameter1 + ' and ' + parameter2 + ' [' + yun + ']')
		ax1.set_ylabel(ylabel);
		figname = filename + '_mean_of_' + parameter1 + '_' + parameter2 + '_nodes.png'
	
	if ymin is not None:
		ax1.set_ylim(bottom = ymin)	
	if ymax is not None:
		ax1.set_ylim(top = ymax)
		
	if turns is not None: 
		ax1.set_xlim(left = 0)
		ax1.set_xlim(right = turns)
		
	if legend_label is not None: 
		ax1.legend(title=legend_label)
	else:
		ax1.legend()
		
	ax1.set_xlabel('Turn [-]');
	ax1.set_title(tit);
	ax1.grid(True);
	
	fig1.savefig(figname);
	plt.close()	
	return;

'''
------------------------------------------------------------------------
						Open files and read data
------------------------------------------------------------------------
'''
	
# Create dd dictionary
dd = dict()
dd = add_input_file(dd, './624_SbS/output/output.mat', '6.24')
dd = add_input_file(dd, './622_SbS/output/output.mat', '6.22')
dd = add_input_file(dd, './620_SbS/output/output.mat', '6.20')
dd = add_input_file(dd, './618_SbS/output/output.mat', '6.18')
dd = add_input_file(dd, './616_SbS/output/output.mat', '6.16')
dd = add_input_file(dd, './614_SbS/output/output.mat', '6.14')
dd = add_input_file(dd, './612_SbS/output/output.mat', '6.12')
dd = add_input_file(dd, './610_SbS/output/output.mat', '6.10')
print 'Final data dictionary keys: ', dd.keys()
		
main_label = 'Slice_By_Slice'
legend_label = 'Tune'
turn_tot = None
turns = [0, 1, 10, 100, 199, 874, 2185]

'''
------------------------------------------------------------------------
								Plot
------------------------------------------------------------------------
'''

plot_parameter(dd, parameter = 'intensity', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'intensity', filename = main_label,  percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'mean_x', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'mean_x', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'mean_xp', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'mean_xp', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'mean_y', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'mean_y', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'mean_yp', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'mean_yp', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'mean_z', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'mean_z', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'mean_dE', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'mean_dE', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'epsn_x', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label, ymin=1, ymax=2.2)
plot_parameter(dd, parameter = 'epsn_x', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'epsn_y', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'epsn_y', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'eps_z', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'eps_z', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'bunchlength', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'bunchlength', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'dpp_rms', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'dpp_rms', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_mean_of_two_parameters(dd, parameter1 = 'epsn_x', parameter2 = 'epsn_y', filename = main_label,  legend_label = legend_label)

plot_emittance(dd, main_label, turns, legend_label='Turn', ymin=0.6, ymax=3.8)
