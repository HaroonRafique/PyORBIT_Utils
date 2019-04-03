# Plots all available plottable data from output.mat as individual files
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio 

plt.rcParams['figure.figsize'] = [8.0, 4.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.rcParams['font.size'] = 10
plt.rcParams['legend.fontsize'] = 'medium'
plt.rcParams['lines.linewidth'] = 1

'''
plot_parameter: Required arguments:
parameter name: e.g. 'bunchlength'.
filename: 		e.g. 'Testing' gives Testing_bunchlength.png.

Optional arguments:
percentage:		switch used to plot raw or percentage change from initial value.
lengend_label:	title for legend
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
def plot_parameter(parameter, filename, percentage = False, ymin=None, ymax=None, ylab=None, yun = None, tit = None, multi=None, turns = None):
	
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

	if percentage:
		ax1.plot(particles['turn'][0], ((particles[parameter][0]/particles[parameter][0][0])*100)-100, label=parameter);
		ylabel = str(ylabel + ' percentage change [%]')		
		figname = filename + '_' + parameter + '_percentage'
	else:
		ax1.plot(particles['turn'][0], particles[parameter][0]*multiplier);
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
	
	fig1.savefig(figname);	
	plt.close()
	return;
	
'''
plot_mean_of_two_parameters: Required arguments:
parameter1 name: 	e.g. 'epsn_x'.
parameter1 name: 	e.g. 'epsn_y'.
filename: 			e.g. 'Testing' gives Testing_bunchlength.png.

Optional arguments:
tit:				plot title
ylab:				y-axis label
yun:				y-axis unit
y limits are default unless 'ymin' and 'ymax' arguments are specified.
x limits may be changed with 'turns' argument.

The only expected parameters are epsn_x and epsn_y
'''
def plot_mean_of_two_parameters(parameter1, parameter2, filename, tit=None, ylab=None, yunit='-', ymin=None, ymax=None, turns = None):

	print '\nPlotting mean of ', parameter1, 'and', parameter2,
		
	fig1 = plt.figure(facecolor='w', edgecolor='k')
	ax1 = fig1.add_subplot(111)
			
	if ylab is None:
		ylab = 'mean of ' + parameter1 + ' and ' + parameter2
		
	if tit is None:
		tit = 'mean of ' + parameter1 + ' and ' + parameter2
		
	if 'epsn' in parameter1 and parameter2:
		multiplier = 1./1E-6
		tit = r'$\left(\frac{\epsilon_x^n + \epsilon_y^n}{2}\right)$'
		ylabel = r'$\left(\frac{\epsilon_x^n + \epsilon_y^n}{2}\right)$'
		yunit = '[mm mrad]'
		
		ax1.plot(particles['turn'][0], (particles[parameter1][0]*multiplier + particles[parameter2][0]*multiplier)/2);
		ylabel = ylabel + ' ' + yunit
		ax1.set_ylabel(ylabel);
		figname = filename + '_mean_of_' + parameter1 + '_' + parameter2 + '_nodes.png'
	else:
		ax1.plot(particles['turn'][0], (particles[parameter1][0] + particles[parameter2][0])/2);
		ylabel = str( 'mean of ' + parameter1 + ' and ' + parameter2 + ' [' + yunit + ']')
		ax1.set_ylabel(ylabel);
		figname = filename + '_mean_of_' + parameter1 + '_' + parameter2 + '_nodes.png'
	
	if ymin is not None:
		ax1.set_ylim(bottom = ymin)	
	if ymax is not None:
		ax1.set_ylim(top = ymax)
		
	if turns is not None: 
		ax1.set_xlim(left = 0)
		ax1.set_xlim(right = turns)
		
	ax1.set_xlabel('Turn [-]');
	ax1.set_title(tit);
	ax1.grid(True);
	
	fig1.savefig(figname);	
	plt.close()
	return;


###########################
# Open file and read data #
###########################

file_in = 'output.mat'
main_label = 'Testing'
turn_tot = 10000

particles = dict()
sio.loadmat(file_in, mdict=particles)

# Parameters
# ~ output.addParameter('turn', lambda: turn)
# ~ output.addParameter('intensity', lambda: bunchtwissanalysis.getGlobalMacrosize())
# ~ output.addParameter('n_mp', lambda: bunchtwissanalysis.getGlobalCount())
# ~ output.addParameter('gamma', lambda: bunch.getSyncParticle().gamma())
# ~ output.addParameter('mean_x', lambda: bunchtwissanalysis.getAverage(0))
# ~ output.addParameter('mean_xp', lambda: bunchtwissanalysis.getAverage(1))
# ~ output.addParameter('mean_y', lambda: bunchtwissanalysis.getAverage(2))
# ~ output.addParameter('mean_yp', lambda: bunchtwissanalysis.getAverage(3))
# ~ output.addParameter('mean_z', lambda: bunchtwissanalysis.getAverage(4))
# ~ output.addParameter('mean_dE', lambda: bunchtwissanalysis.getAverage(5))
# ~ output.addParameter('epsn_x', lambda: bunchtwissanalysis.getEmittanceNormalized(0))
# ~ output.addParameter('epsn_y', lambda: bunchtwissanalysis.getEmittanceNormalized(1))
# ~ output.addParameter('eps_z', lambda: get_eps_z(bunch, bunchtwissanalysis))
# ~ output.addParameter('bunchlength', lambda: get_bunch_length(bunch, bunchtwissanalysis))
# ~ output.addParameter('dpp_rms', lambda: get_dpp(bunch, bunchtwissanalysis))

plot_parameter(parameter = 'intensity', filename = main_label, percentage = False)
plot_parameter(parameter = 'intensity', filename = main_label, percentage = True)

plot_parameter(parameter = 'mean_x', filename = main_label, percentage = False)
plot_parameter(parameter = 'mean_x', filename = main_label, percentage = True)

plot_parameter(parameter = 'mean_xp', filename = main_label, percentage = False)
plot_parameter(parameter = 'mean_xp', filename = main_label, percentage = True)

plot_parameter(parameter = 'mean_y', filename = main_label, percentage = False)
plot_parameter(parameter = 'mean_y', filename = main_label, percentage = True)

plot_parameter(parameter = 'mean_yp', filename = main_label, percentage = False)
plot_parameter(parameter = 'mean_yp', filename = main_label, percentage = True)

plot_parameter(parameter = 'mean_z', filename = main_label, percentage = False)
plot_parameter(parameter = 'mean_z', filename = main_label, percentage = True)

plot_parameter(parameter = 'mean_dE', filename = main_label, percentage = False)
plot_parameter(parameter = 'mean_dE', filename = main_label, percentage = True)

plot_parameter(parameter = 'epsn_x', filename = main_label, percentage = False)
plot_parameter(parameter = 'epsn_x', filename = main_label, percentage = True)

plot_parameter(parameter = 'epsn_y', filename = main_label, percentage = False)
plot_parameter(parameter = 'epsn_y', filename = main_label, percentage = True)

plot_parameter(parameter = 'eps_z', filename = main_label, percentage = False)
plot_parameter(parameter = 'eps_z', filename = main_label, percentage = True)

plot_parameter(parameter = 'bunchlength', filename = main_label, percentage = False)
plot_parameter(parameter = 'bunchlength', filename = main_label,percentage = True)

plot_parameter(parameter = 'dpp_rms', filename = main_label, percentage = False)
plot_parameter(parameter = 'dpp_rms', filename = main_label, percentage = True)

plot_mean_of_two_parameters(parameter1 = 'epsn_x', parameter2 = 'epsn_y', filename = main_label, yunit = 'm rad')
