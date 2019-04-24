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
	print '\tAdded output data from ', filename, '\t dictionary key: ', label
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
output.addParameter('beta_x', lambda: bunchtwissanalysis.getBeta(0))
output.addParameter('beta_y', lambda: bunchtwissanalysis.getBeta(1))
output.addParameter('alpha_x', lambda: bunchtwissanalysis.getAlpha(0))
output.addParameter('alpha_y', lambda: bunchtwissanalysis.getAlpha(1))
output.addParameter('D_x', lambda: bunchtwissanalysis.getDispersion(0))
output.addParameter('D_y', lambda: bunchtwissanalysis.getDispersion(1))
output.addParameter('eff_beta_x', lambda: bunchtwissanalysis.getEffectiveBeta(0))
output.addParameter('eff_beta_y', lambda: bunchtwissanalysis.getEffectiveBeta(1))
output.addParameter('eff_epsn_x', lambda: bunchtwissanalysis.getEffectiveEmittance(0))
output.addParameter('eff_epsn_y', lambda: bunchtwissanalysis.getEffectiveEmittance(1))
output.addParameter('eff_alpha_x', lambda: bunchtwissanalysis.getEffectiveAlpha(0))
output.addParameter('eff_alpha_y', lambda: bunchtwissanalysis.getEffectiveAlpha(1))

------------------------------------------------------------------------
'''
def plot_parameter(dd, parameter, filename, percentage = False, ymin=None, ymax=None, ylab=None, yun = None, tit = None, multi=None, turns = None, legend_label = None, betagamma = None):
		
	if percentage:
		print 'Plotting ', parameter, ' percentage'
	else:
		print 'Plotting ', parameter
	
	if betagamma is None: betagamma = 2.492104532 * 0.9159915293879255
	
	multiplier = 1.

	fig1 = plt.figure(facecolor='w', edgecolor='k')
	ax1 = fig1.add_subplot(111)
	
	if parameter is 'bunchlength':
		multiplier = 1./1E-9
		ylabel = r'$B_l$' 
		yunit = '[ns]'
		ax1.set_title('Bunch Length');
		figname = filename + '_' + parameter
		
	elif parameter is 'eff_beta_x':
		ylabel = r'Effective $\beta_x$' 
		yunit = '[m]'
		ax1.set_title(r'Effective $\beta_x$');
		figname = filename + '_' + parameter	
		
	elif parameter is 'eff_beta_y':
		ylabel = r'Effective $\beta_y$' 
		yunit = '[m]'
		ax1.set_title(r'Effective $\beta_y$');
		figname = filename + '_' + parameter	
		
	elif parameter is 'eff_alpha_x':
		ylabel = r'Effective $\alpha_x$' 
		yunit = '[-]'
		ax1.set_title(r'Effective $\alpha_x$');
		figname = filename + '_' + parameter	
		
	elif parameter is 'eff_alpha_y':
		ylabel = r'Effective $\alpha_y$' 
		yunit = '[-]'
		ax1.set_title(r'Effective $\alpha_y$');
		figname = filename + '_' + parameter	
		
	elif parameter is 'beta_x':
		ylabel = r'$\beta_x$' 
		yunit = '[m]'
		ax1.set_title(r'$\beta_x$');
		figname = filename + '_' + parameter	
		
	elif parameter is 'beta_y':
		ylabel = r'$\beta_y$' 
		yunit = '[m]'
		ax1.set_title(r' $\beta_y$');
		figname = filename + '_' + parameter	
		
	elif parameter is 'D_x':
		ylabel = r'D$_x$' 
		yunit = '[m]'
		ax1.set_title(r'D$_x$');
		figname = filename + '_' + parameter	
		
	elif parameter is 'D_y':
		ylabel = r'D$_y$' 
		yunit = '[m]'
		ax1.set_title(r'D$_y$');
		figname = filename + '_' + parameter	
		
	elif parameter is 'alpha_x':
		ylabel = r'$\alpha_x$' 
		yunit = '[-]'
		ax1.set_title(r'$\alpha_x$');
		figname = filename + '_' + parameter	
		
	elif parameter is 'alpha_y':
		ylabel = r'$\alpha_y$' 
		yunit = '[-]'
		ax1.set_title(r'$\alpha_y$');
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
		
	elif parameter is 'eff_epsn_x':		
		multiplier = betagamma/1E-6
		ylabel = r'Effective $\epsilon_x^n$'
		yunit = '[mm mrad]'
		ax1.set_title('Effective Horizontal Emittance');
		figname = filename + '_' + parameter
		
	elif parameter is 'eff_epsn_y':
		betagamma = 2.492104532 * 0.9159915293879255
		multiplier = betagamma/1E-6
		ylabel = r'Effective $\epsilon_y^n$'
		yunit = '[mm mrad]'
		ax1.set_title('Effective Vertical Emittance');
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
plot_two_parameters: Required arguments:
dd: dictionary of particle data dictionaries. key = user defined label
parameter1: 	e.g. 'epsn_x'.
parameter1: 	e.g. 'eff_epsn_x'.
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
output.addParameter('turn', lambda: turn)
output.addParameter('epsn_x', lambda: bunchtwissanalysis.getEmittanceNormalized(0))
output.addParameter('epsn_y', lambda: bunchtwissanalysis.getEmittanceNormalized(1))
output.addParameter('beta_x', lambda: bunchtwissanalysis.getBeta(0))
output.addParameter('beta_y', lambda: bunchtwissanalysis.getBeta(1))
output.addParameter('alpha_x', lambda: bunchtwissanalysis.getAlpha(0))
output.addParameter('alpha_y', lambda: bunchtwissanalysis.getAlpha(1))
output.addParameter('eff_beta_x', lambda: bunchtwissanalysis.getEffectiveBeta(0))
output.addParameter('eff_beta_y', lambda: bunchtwissanalysis.getEffectiveBeta(1))
output.addParameter('eff_epsn_x', lambda: bunchtwissanalysis.getEffectiveEmittance(0))
output.addParameter('eff_epsn_y', lambda: bunchtwissanalysis.getEffectiveEmittance(1))
output.addParameter('eff_alpha_x', lambda: bunchtwissanalysis.getEffectiveAlpha(0))
output.addParameter('eff_alpha_y', lambda: bunchtwissanalysis.getEffectiveAlpha(1))
'''
def plot_two_parameters (dd, parameter1, parameter2, filename, ymin=None, ymax=None, ylab=None, yun = None, tit = None, multi=None, turns = None, legend_label = None, betagamma = None):
	
	print 'Plotting ', parameter1, ' and' , parameter2
	
	if betagamma is None: betagamma = 2.492104532 * 0.9159915293879255
	
	multiplier1 = 1.
	multiplier2 = 1.

	fig1 = plt.figure(facecolor='w', edgecolor='k')
	ax1 = fig1.add_subplot(111)

	# betas, emittances, alphas
	if (parameter1 is 'beta_x' and parameter2 is 'eff_beta_x') or (parameter2 is 'beta_x' and parameter1 is 'eff_beta_x'):
		ylabel = r'$\beta_x$' 
		yunit = '[m]'
		ax1.set_title(r'$\beta_x$');
		figname = filename + '_' + parameter1 + '_and_' + parameter2
		print '\t beta_x and eff_beta_x'
		
	elif (parameter1 is 'beta_y' and parameter2 is 'eff_beta_y') or (parameter2 is 'beta_y' and parameter1 is 'eff_beta_y'):
		ylabel = r'$\beta_y$' 
		yunit = '[m]'
		ax1.set_title(r' $\beta_y$');
		figname = filename + '_' + parameter1 + '_and_' + parameter2
		print '\t beta_y and eff_beta_y'
		
	elif 'beta' in parameter1 and parameter2:
		ylabel = r'$\beta$' 
		yunit = '[m]'
		ax1.set_title(r' $\beta$');
		figname = filename + '_' + parameter1 + '_and_' + parameter2	
		print '\t beta and beta'
		
	elif (parameter1 is 'epsn_x' and parameter2 is 'eff_epsn_x') or (parameter2 is 'epsn_x' and parameter1 is 'eff_epsn_x'):
		if parameter1 is 'epsn_x' and parameter2 is 'eff_epsn_x':
			multiplier1 = 1./1E-6
			multiplier2 = betagamma/1E-6
			print '\t epsn_x and eff_epsn_x'
			
		elif parameter2 is 'epsn_x' and parameter1 is 'eff_epsn_x':
			multiplier1 = betagamma/1E-6
			multiplier2 = 1./1E-6
			print '\t eff_epsn_x and epsn_x'
		
		ax1.set_title('Horizontal Emittance');
		ylabel = r'$\epsilon^n$'
		yunit = '[mm mrad]'
		ax1.set_title('Emittance');
		figname = filename + '_' + parameter1 + '_and_' + parameter2	
					
	elif (parameter1 is 'epsn_y' and parameter2 is 'eff_epsn_y') or (parameter2 is 'epsn_y' and parameter1 is 'eff_epsn_y'):
		if parameter1 is 'epsn_y' and parameter2 is 'eff_epsn_y':
			multiplier1 = 1./1E-6
			multiplier2 = betagamma/1E-6
			print '\t epsn_y and eff_epsn_y'
			
		elif parameter2 is 'epsn_y' and parameter1 is 'eff_epsn_y':
			multiplier1 = betagamma/1E-6
			multiplier2 = 1./1E-6
			print '\t eff_epsn_y and epsn_y'
				
		ax1.set_title('Vertical Emittance');
		ylabel = r'$\epsilon^n$'
		yunit = '[mm mrad]'
		ax1.set_title('Emittance');
		figname = filename + '_' + parameter1 + '_and_' + parameter2	

	elif ('epsn' in parameter1 and parameter2) and ('eff' not in parameter1 or parameter2):		
		multiplier1 = 1./1E-6
		multiplier2 = 1./1E-6
		ylabel = r'$\epsilon^n$'
		yunit = '[mm mrad]'
		ax1.set_title('Emittance');
		figname = filename + '_' + parameter1 + '_and_' + parameter2			
		
	elif (parameter1 is 'alpha_x' and parameter2 is 'eff_alpha_x') or (parameter2 is 'alpha_x' and parameter1 is 'eff_alpha_x'):
		ylabel = r'$\alpha_x$' 
		yunit = '[-]'
		ax1.set_title(r'$\alpha_x$');
		figname = filename + '_' + parameter1 + '_and_' + parameter2
		print '\t alpha_x and eff_alpha_x'
	
	elif (parameter1 is 'alpha_y' and parameter2 is 'eff_alpha_y') or (parameter2 is 'alpha_y' and parameter1 is 'eff_alpha_y'):
		ylabel = r'$\alpha_y$' 
		yunit = '[-]'
		ax1.set_title(r'$\alpha_y$');
		figname = filename + '_' + parameter1 + '_and_' + parameter2	
		print '\t alpha_y and eff_alpha_y'
		
	elif 'alpha' in parameter1 and parameter2:
		ylabel = r'$\alpha$' 
		yunit = '[-]'
		ax1.set_title(r'$\alpha$');
		figname = filename + '_' + parameter1 + '_and_' + parameter2
		print '\t alphas'
		
	else:
		multiplier = multi
		ylabel = ylab
		yunit = yun
		ax1.set_title(tit);
		figname = filename + '_' + parameter1 + '_and_' + parameter2
		print '\t Standard plot'

	colors = cm.rainbow(np.linspace(0, 1, len(dd.keys())))
	c_it = int(0)	
	
	for key, value in sorted(dd.iteritems()):			
		ax1.plot(dd[key]['turn'][0], dd[key][parameter1][0]*multiplier1, label=key, color=colors[c_it]);
		ax1.plot(dd[key]['turn'][0], dd[key][parameter2][0]*multiplier2, label=key, color=colors[c_it], linestyle='dashed');
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
plot_effective_sigmas: Required arguments:
dd: dictionary of particle data dictionaries. key = user defined label
filename: 			e.g. 'Testing' gives Testing_bunchlength.png.
Optional arguments:
Real:				Flag to use beta and epsn instead of effective values
tit:				plot title
ylab:				y-axis label
yun:				y-axis unit
legend_label:		title for legend
y limits are default unless 'ymin' and 'ymax' arguments are specified.
x limits may be changed with 'turns' argument.
'''
def plot_effective_sigmas(dd, filename, ymin=None, ymax=None, ylab=None, yun = None, tit = None, turns = None, legend_label = None, real = False, betagamma = None):

	if real:
		print 'Plotting real sigma'
	else:
		print 'Plotting effective sigma'
		
	
	if betagamma is None: betagamma = 2.492104532 * 0.9159915293879255
	
	multiplier = 1.

	fig1 = plt.figure(facecolor='w', edgecolor='k')
	ax1 = fig1.add_subplot(111)
	
	if real: 
		ax1.set_title('Horizontal Bunch Size');
		figname = filename + '_sigma_x'
	else:
		ax1.set_title('Effective Horizontal Bunch Size');
		figname = filename + '_effective_sigma_x'
		
	multiplier = 1./1E-3
	ylabel = r'$\sigma_x$' 
	yunit = r'[mm]'

	colors = cm.rainbow(np.linspace(0, 1, len(dd.keys())))
	c_it = int(0)		

	for key, value in sorted(dd.iteritems()):	
		if real:		
			ax1.plot(dd[key]['turn'][0], np.sqrt(dd[key]['beta_x'][0] * (dd[key]['epsn_x'][0]/betagamma))*multiplier, label=key, color=colors[c_it]);
		else:
			ax1.plot(dd[key]['turn'][0], np.sqrt(dd[key]['eff_beta_x'][0] * dd[key]['eff_epsn_x'][0])*multiplier, label=key, color=colors[c_it]);
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
	
	fig2 = plt.figure(facecolor='w', edgecolor='k')
	ax2 = fig2.add_subplot(111)	
		
	if real: 
		ax2.set_title('Vertical Bunch Size');
		figname = filename + '_sigma_y'
	else:
		ax2.set_title('Effective Vertical Bunch Size');
		figname = filename + '_effective_sigma_y'
	
	multiplier = 1./1E-3
	ylabel = r'$\sigma_y$' 
	yunit = r'[mm]'

	colors = cm.rainbow(np.linspace(0, 1, len(dd.keys())))
	c_it = int(0)		

	for key, value in sorted(dd.iteritems()):			
		if real:
			ax2.plot(dd[key]['turn'][0], np.sqrt(dd[key]['beta_y'][0] * (dd[key]['epsn_y'][0]/betagamma))*multiplier, label=key, color=colors[c_it]);
		else:
			ax2.plot(dd[key]['turn'][0], np.sqrt(dd[key]['eff_beta_y'][0] * dd[key]['eff_epsn_y'][0])*multiplier, label=key, color=colors[c_it]);
		c_it = c_it + 1
	ylabel = str(ylabel + ' ' + yunit)
		
	if ymin is not None:
		ax2.set_ylim(bottom = ymin)	
	if ymax is not None:
		ax2.set_ylim(top = ymax)
		
	if turns is not None: 
		ax2.set_xlim(left = 0)
		ax2.set_xlim(right = turns)
	
	ax2.set_ylabel(ylabel);
	ax2.set_xlabel('Turn [-]');
	ax2.grid(True);
	
	figname = figname + '.png'
	
	if legend_label is not None: 
		ax2.legend(title=legend_label)
	else:
		ax2.legend()
		
	fig2.savefig(figname);	
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
def plot_mean_of_two_parameters(dd, parameter1, parameter2, filename, tit=None, ylab=None, yun='-', ymin=None, ymax=None, turns = None, legend_label = None, betagamma = None):

	print 'Plotting mean of ', parameter1, 'and', parameter2
	
	if betagamma is None: betagamma = 2.492104532 * 0.9159915293879255
		
	fig1 = plt.figure(figsize=(6,4))
	ax1 = fig1.add_subplot(111)
	
			
	if ylab is None:
		ylab = 'mean of ' + parameter1 + ' and ' + parameter2
		
	if tit is None:
		tit = 'mean of ' + parameter1 + ' and ' + parameter2
				
	colors = cm.rainbow(np.linspace(0, 1, len(dd.keys())))
	c_it = int(0)	
		
	if parameter1 is parameter2:
		print '\tWARNING: plot_mean_of_two_parameters has been given the same parameter ' + parameter1 + ' twice'
	
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
		
	elif 'eff' in parameter1 or parameter2: 
		multiplier = 1./1E-6
		tit = r'$\left(\frac{\epsilon_x^n + \epsilon_y^n}{2}\right)$'
		ylabel = r'$\left(\frac{\epsilon_x^n + \epsilon_y^n}{2}\right)$'
		yun = '[mm mrad]'	
		
		if 'eff' in parameter1 and parameter2:			
			multiplier1 = betagamma/1E-6
			for key, value in sorted(dd.iteritems()):		
				ax1.plot(dd[key]['turn'][0], (dd[key][parameter1][0]*multiplier1 + dd[key][parameter2][0]*multiplier1)/2, label=key, color=colors[c_it]);
				c_it = c_it + 1
			
		elif 'eff' in parameter1:
			multiplier1 = betagamma/1E-6
			for key, value in sorted(dd.iteritems()):		
				ax1.plot(dd[key]['turn'][0], (dd[key][parameter1][0]*multiplier1 + dd[key][parameter2][0]*multiplier)/2, label=key, color=colors[c_it]);
				c_it = c_it + 1
			
		elif 'eff' in parameter2:
			multiplier2 = betagamma/1E-6
			for key, value in sorted(dd.iteritems()):		
				ax1.plot(dd[key]['turn'][0], (dd[key][parameter1][0]*multiplier + dd[key][parameter2][0]*multiplier2)/2, label=key, color=colors[c_it]);
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

dd = add_input_file(dd, './Grid/32_32_16/output/output.mat', '32x32x16_SbS')
dd = add_input_file(dd, './Grid/64_64_32/output/output.mat', '64x64x32_SbS')
dd = add_input_file(dd, './Grid/128_128_64/output/output.mat', '128x128x64_SbS')
dd = add_input_file(dd, './Grid/256_256_128/output/output.mat', '256x256x128_SbS')
# ~ main_label = 'Convergence_GridSize_SbS'
# ~ main_label2 = 'Convergence_GridSize_SbS_zoom'

dd = add_input_file(dd, './Grid_2p5/32_32_16/output/output.mat', '32x32x16_2.5D')
dd = add_input_file(dd, './Grid_2p5/64_64_32/output/output.mat', '64x64x32_2.5D')
dd = add_input_file(dd, './Grid_2p5/128_128_64/output/output.mat', '128x128x64_2.5D')
dd = add_input_file(dd, './Grid_2p5/256_256_128/output/output.mat', '256x256x128_2.5D')
# ~ main_label = 'Convergence_GridSize_2p5'
# ~ main_label2 = 'Convergence_GridSize_2p5_zoom'

dd = add_input_file(dd, './Grid_nLK/32_32_16/output/output.mat', '32x32x16_nLK')
dd = add_input_file(dd, './Grid_nLK/64_64_32/output/output.mat', '64x64x32_nLK')
dd = add_input_file(dd, './Grid_nLK/128_128_64/output/output.mat', '128x128x64_nLK')
dd = add_input_file(dd, './Grid_nLK/256_256_128/output/output.mat', '256x256x128_nLK')
# ~ main_label = 'Convergence_GridSize_nLK'
# ~ main_label2 = 'Convergence_GridSize_nLK_zoom'

main_label = 'Convergence_GridSize'
main_label2 = 'Convergence_GridSize_zoom'

legend_label = 'Grid Size'
turn_tot = None
zoom_turns = 15
turns = [0, 1, 10, 100, 199, 874, 2185]
print 'Final data dictionary keys: ', dd.keys()

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

plot_parameter(dd, parameter = 'epsn_x', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)#, ymin=1, ymax=2.5)
plot_parameter(dd, parameter = 'epsn_x', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'epsn_y', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)#, ymin=1, ymax=2.5)
plot_parameter(dd, parameter = 'epsn_y', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'eff_epsn_x', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)#, ymin=1, ymax=2.5)
plot_parameter(dd, parameter = 'eff_epsn_x', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'eff_epsn_y', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)#, ymin=1, ymax=2.5)
plot_parameter(dd, parameter = 'eff_epsn_y', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'eps_z', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'eps_z', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'bunchlength', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'bunchlength', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'dpp_rms', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'dpp_rms', filename = main_label, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'beta_x', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'beta_y', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'alpha_x', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'alpha_y', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'eff_beta_x', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'eff_beta_y', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'eff_alpha_x', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'eff_alpha_y', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)

plot_parameter(dd, parameter = 'D_x', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(dd, parameter = 'D_y', filename = main_label, percentage = False, turns = turn_tot, legend_label = legend_label)

# Effective Sigma

plot_effective_sigmas(dd, main_label, turns = turn_tot, legend_label = legend_label, real=False)
plot_effective_sigmas(dd, main_label, turns = turn_tot, legend_label = legend_label, real=True)

# Zoom plots

plot_parameter(dd, parameter = 'eff_beta_x', filename = main_label2, percentage = False, turns = zoom_turns, legend_label = legend_label)
plot_parameter(dd, parameter = 'eff_beta_y', filename = main_label2, percentage = False, turns = zoom_turns, legend_label = legend_label)

plot_parameter(dd, parameter = 'eff_alpha_x', filename = main_label2, percentage = False, turns = zoom_turns, legend_label = legend_label)
plot_parameter(dd, parameter = 'eff_alpha_y', filename = main_label2, percentage = False, turns = zoom_turns, legend_label = legend_label)

plot_parameter(dd, parameter = 'beta_x', filename = main_label2, percentage = False, turns = zoom_turns, legend_label = legend_label)
plot_parameter(dd, parameter = 'beta_y', filename = main_label2, percentage = False, turns = zoom_turns, legend_label = legend_label)

plot_parameter(dd, parameter = 'alpha_x', filename = main_label2, percentage = False, turns = zoom_turns, legend_label = legend_label)
plot_parameter(dd, parameter = 'alpha_y', filename = main_label2, percentage = False, turns = zoom_turns, legend_label = legend_label)

plot_parameter(dd, parameter = 'D_x', filename = main_label2, percentage = False, turns = zoom_turns, legend_label = legend_label)
plot_parameter(dd, parameter = 'D_y', filename = main_label2, percentage = False, turns = zoom_turns, legend_label = legend_label)

# Two parameter plots

plot_two_parameters(dd, 'epsn_x', 'eff_epsn_x', filename = main_label, turns = turn_tot, legend_label = legend_label)
plot_two_parameters(dd, 'epsn_y', 'eff_epsn_y', filename = main_label, turns = turn_tot, legend_label = legend_label)

plot_two_parameters(dd, 'beta_x', 'eff_beta_x', filename = main_label, turns = turn_tot, legend_label = legend_label)
plot_two_parameters(dd, 'beta_y', 'eff_beta_y', filename = main_label, turns = turn_tot, legend_label = legend_label)

plot_two_parameters(dd, 'alpha_x', 'eff_alpha_x', filename = main_label, turns = turn_tot, legend_label = legend_label)
plot_two_parameters(dd, 'alpha_y', 'eff_alpha_y', filename = main_label, turns = turn_tot, legend_label = legend_label)


# Mean of epsn_x and epsn_y

plot_mean_of_two_parameters(dd, parameter1 = 'epsn_x', parameter2 = 'epsn_y', filename = main_label,  legend_label = legend_label)

plot_mean_of_two_parameters(dd, parameter1 = 'eff_epsn_x', parameter2 = 'eff_epsn_y', filename = main_label,  legend_label = legend_label)

# Emittances

# ~ plot_emittance(dd, main_label, turns, legend_label='Turn')
