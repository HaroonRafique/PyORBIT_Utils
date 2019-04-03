# Plots all available plottable data from output.mat as individual files
import matplotlib.pyplot as plt
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
plot_parameter: Required arguments:
parameter name: e.g. 'bunchlength'.
filename: 		e.g. 'Testing' gives Testing_bunchlength.png.
n_files: 		number of input files (int).
labels:			labels for each input file (array of strings).

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
def plot_parameter(parameter, filename, n_files, labels, percentage = False, ymin=None, ymax=None, ylab=None, yun = None, tit = None, multi=None, turns = None, legend_label = None):
	
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


	colors = cm.rainbow(np.linspace(0, 1, n_files))

	if percentage:
		if n_files > 0:	ax1.plot(particles_1['turn'][0], ((particles_1[parameter][0]/particles_1[parameter][0][0])*100)-100, label=labels[0], color=colors[0]);
		if n_files > 1:	ax1.plot(particles_2['turn'][0], ((particles_2[parameter][0]/particles_2[parameter][0][0])*100)-100, label=labels[1], color=colors[1]);
		if n_files > 2:	ax1.plot(particles_3['turn'][0], ((particles_3[parameter][0]/particles_3[parameter][0][0])*100)-100, label=labels[2], color=colors[2]);
		if n_files > 3:	ax1.plot(particles_4['turn'][0], ((particles_4[parameter][0]/particles_4[parameter][0][0])*100)-100, label=labels[3], color=colors[3]);
		if n_files > 4:	ax1.plot(particles_5['turn'][0], ((particles_5[parameter][0]/particles_5[parameter][0][0])*100)-100, label=labels[4], color=colors[4]);
		if n_files > 5:	ax1.plot(particles_6['turn'][0], ((particles_6[parameter][0]/particles_6[parameter][0][0])*100)-100, label=labels[5], color=colors[5]);
		if n_files > 6:	ax1.plot(particles_7['turn'][0], ((particles_7[parameter][0]/particles_7[parameter][0][0])*100)-100, label=labels[6], color=colors[6]);
		if n_files > 7:	ax1.plot(particles_8['turn'][0], ((particles_8[parameter][0]/particles_8[parameter][0][0])*100)-100, label=labels[7], color=colors[7]);
		if n_files > 8:	ax1.plot(particles_9['turn'][0], ((particles_9[parameter][0]/particles_9[parameter][0][0])*100)-100, label=labels[8], color=colors[8]);
		if n_files > 9:	ax1.plot(particles_10['turn'][0], ((particles_10[parameter][0]/particles_10[parameter][0][0])*100)-100, label=labels[9], color=colors[9]);
		if n_files > 10: 
			print '\nWARNING: Number of files exceeds limit. Exiting.\n'
			exit(0)
			
		ylabel = str(ylabel + ' percentage change [%]')		
		figname = filename + '_' + parameter + '_percentage'
	else:
		
		if n_files > 0:	ax1.plot(particles_1['turn'][0], particles_1[parameter][0]*multiplier, label=labels[0], color=colors[0]);
		if n_files > 1:	ax1.plot(particles_2['turn'][0], particles_2[parameter][0]*multiplier, label=labels[1], color=colors[1]);
		if n_files > 2:	ax1.plot(particles_3['turn'][0], particles_3[parameter][0]*multiplier, label=labels[2], color=colors[2]);
		if n_files > 3:	ax1.plot(particles_4['turn'][0], particles_4[parameter][0]*multiplier, label=labels[3], color=colors[3]);
		if n_files > 4:	ax1.plot(particles_5['turn'][0], particles_5[parameter][0]*multiplier, label=labels[4], color=colors[4]);
		if n_files > 5:	ax1.plot(particles_6['turn'][0], particles_6[parameter][0]*multiplier, label=labels[5], color=colors[5]);
		if n_files > 6:	ax1.plot(particles_7['turn'][0], particles_7[parameter][0]*multiplier, label=labels[6], color=colors[6]);
		if n_files > 7:	ax1.plot(particles_8['turn'][0], particles_8[parameter][0]*multiplier, label=labels[7], color=colors[7]);
		if n_files > 8:	ax1.plot(particles_9['turn'][0], particles_9[parameter][0]*multiplier, label=labels[8], color=colors[8]);
		if n_files > 9:	ax1.plot(particles_10['turn'][0], particles_10[parameter][0]*multiplier, label=labels[9], color=colors[9]);
		if n_files > 10: 
			print '\nWARNING: Number of files exceeds limit. Exiting.\n'
			exit(0)
			
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
parameter1 name: 	e.g. 'epsn_x'.
parameter1 name: 	e.g. 'epsn_y'.
filename: 			e.g. 'Testing' gives Testing_bunchlength.png.
n_files: 			number of input files (int).
labels:				labels for each input file (array of strings).

Optional arguments:
tit:				plot title
ylab:				y-axis label
yun:				y-axis unit
legend_label:		title for legend
y limits are default unless 'ymin' and 'ymax' arguments are specified.
x limits may be changed with 'turns' argument.

The only expected parameters are epsn_x and epsn_y
'''
def plot_mean_of_two_parameters(parameter1, parameter2, filename, n_files, labels, tit=None, ylab=None, yun='-', ymin=None, ymax=None, turns = None, legend_label = None):

	print '\nPlotting mean of ', parameter1, 'and', parameter2,
		
	fig1 = plt.figure(figsize=(6,4))
	ax1 = fig1.add_subplot(111)
	
			
	if ylab is None:
		ylab = 'mean of ' + parameter1 + ' and ' + parameter2
		
	if tit is None:
		tit = 'mean of ' + parameter1 + ' and ' + parameter2
				
	colors = cm.rainbow(np.linspace(0, 1, n_files))
		
	if 'epsn' in parameter1 and parameter2:
		multiplier = 1./1E-6
		tit = r'$\left(\frac{\epsilon_x^n + \epsilon_y^n}{2}\right)$'
		ylabel = r'$\left(\frac{\epsilon_x^n + \epsilon_y^n}{2}\right)$'
		yun = '[mm mrad]'
		
		if n_files > 0:	ax1.plot(particles_1['turn'][0], (particles_1[parameter1][0]*multiplier + particles_1[parameter2][0]*multiplier)/2, label=labels[0], color=colors[0]);
		if n_files > 1:	ax1.plot(particles_2['turn'][0], (particles_2[parameter1][0]*multiplier + particles_2[parameter2][0]*multiplier)/2, label=labels[1], color=colors[1]);
		if n_files > 2:	ax1.plot(particles_3['turn'][0], (particles_3[parameter1][0]*multiplier + particles_3[parameter2][0]*multiplier)/2, label=labels[2], color=colors[2]);
		if n_files > 3:	ax1.plot(particles_4['turn'][0], (particles_4[parameter1][0]*multiplier + particles_4[parameter2][0]*multiplier)/2, label=labels[3], color=colors[3]);
		if n_files > 4:	ax1.plot(particles_5['turn'][0], (particles_5[parameter1][0]*multiplier + particles_5[parameter2][0]*multiplier)/2, label=labels[4], color=colors[4]);
		if n_files > 5:	ax1.plot(particles_6['turn'][0], (particles_6[parameter1][0]*multiplier + particles_6[parameter2][0]*multiplier)/2, label=labels[5], color=colors[5]);
		if n_files > 6:	ax1.plot(particles_7['turn'][0], (particles_7[parameter1][0]*multiplier + particles_7[parameter2][0]*multiplier)/2, label=labels[6], color=colors[6]);
		if n_files > 7:	ax1.plot(particles_8['turn'][0], (particles_8[parameter1][0]*multiplier + particles_8[parameter2][0]*multiplier)/2, label=labels[7], color=colors[7]);
		if n_files > 8:	ax1.plot(particles_9['turn'][0], (particles_9[parameter1][0]*multiplier + particles_9[parameter2][0]*multiplier)/2, label=labels[8], color=colors[8]);
		if n_files > 9:	ax1.plot(particles_10['turn'][0], (particles_10[parameter1][0]*multiplier + particles_10[parameter2][0]*multiplier)/2, label=labels[9], color=colors[9]);
		
		ylabel = ylabel + ' ' + yun
		ax1.set_ylabel(ylabel);
		figname = filename + '_mean_of_' + parameter1 + '_' + parameter2 + '_nodes.png'
	else:
		if n_files > 0:	ax1.plot(particles_1['turn'][0], (particles_1[parameter1][0] + particles_1[parameter2][0])/2, label=labels[0], color=colors[0]);
		if n_files > 1:	ax1.plot(particles_2['turn'][0], (particles_2[parameter1][0] + particles_2[parameter2][0])/2, label=labels[1], color=colors[1]);
		if n_files > 2:	ax1.plot(particles_3['turn'][0], (particles_3[parameter1][0] + particles_3[parameter2][0])/2, label=labels[2], color=colors[2]);
		if n_files > 3:	ax1.plot(particles_4['turn'][0], (particles_4[parameter1][0] + particles_4[parameter2][0])/2, label=labels[3], color=colors[3]);
		if n_files > 4:	ax1.plot(particles_5['turn'][0], (particles_5[parameter1][0] + particles_5[parameter2][0])/2, label=labels[4], color=colors[4]);
		if n_files > 5:	ax1.plot(particles_6['turn'][0], (particles_6[parameter1][0] + particles_6[parameter2][0])/2, label=labels[5], color=colors[5]);
		if n_files > 6:	ax1.plot(particles_7['turn'][0], (particles_7[parameter1][0] + particles_7[parameter2][0])/2, label=labels[6], color=colors[6]);
		if n_files > 7:	ax1.plot(particles_8['turn'][0], (particles_8[parameter1][0] + particles_8[parameter2][0])/2, label=labels[7], color=colors[7]);
		if n_files > 8:	ax1.plot(particles_9['turn'][0], (particles_9[parameter1][0] + particles_9[parameter2][0])/2, label=labels[8], color=colors[8]);
		if n_files > 9:	ax1.plot(particles_10['turn'][0], (particles_10[parameter1][0] + particles_10[parameter2][0])/2, label=labels[9], color=colors[9]);
		
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

labels = ['6.09', '6.10', '6.11', '6.12', '6.13', '6.17', '6.19', '6.21', '6.22', '6.24']
main_label = 'Testing'
legend_label = 'Tune'
turn_tot = 2000
files = 10

if len(labels) != files:
	print '\nWARNING: : Number of files is not equal to number of labels. Please check and correct. Exiting.\n'
	exit(0)

# Open File
file_1='09/output/output.mat'
file_2='10/output/output.mat'
file_3='11/output/output.mat'
file_4='12/output/output.mat'
file_5='13/output/output.mat'
file_6='17/output/output.mat'
file_7='19/output/output.mat'
file_8='21/output/output.mat'
file_9='22/output/output.mat'
file_10='24/output/output.mat'

particles_1=dict()
particles_2=dict()
particles_3=dict()
particles_4=dict()
particles_5=dict()
particles_6=dict()
particles_7=dict()
particles_8=dict()
particles_9=dict()
particles_10=dict()

sio.loadmat(file_1, mdict=particles_1)
sio.loadmat(file_2, mdict=particles_2)
sio.loadmat(file_3, mdict=particles_3)
sio.loadmat(file_4, mdict=particles_4)
sio.loadmat(file_5, mdict=particles_5)
sio.loadmat(file_6, mdict=particles_6)
sio.loadmat(file_7, mdict=particles_7)
sio.loadmat(file_8, mdict=particles_8)
sio.loadmat(file_9, mdict=particles_9)
sio.loadmat(file_10, mdict=particles_10)

'''
------------------------------------------------------------------------
								Plot
------------------------------------------------------------------------
'''

plot_parameter(parameter = 'intensity', filename = main_label, n_files = files, labels = labels, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(parameter = 'intensity', filename = main_label, n_files = files, labels = labels,  percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(parameter = 'mean_x', filename = main_label, n_files = files, labels = labels, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(parameter = 'mean_x', filename = main_label, n_files = files, labels = labels,percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(parameter = 'mean_xp', filename = main_label, n_files = files, labels = labels, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(parameter = 'mean_xp', filename = main_label, n_files = files, labels = labels, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(parameter = 'mean_y', filename = main_label, n_files = files, labels = labels, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(parameter = 'mean_y', filename = main_label, n_files = files, labels = labels, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(parameter = 'mean_yp', filename = main_label, n_files = files, labels = labels, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(parameter = 'mean_yp', filename = main_label, n_files = files, labels = labels, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(parameter = 'mean_z', filename = main_label, n_files = files, labels = labels, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(parameter = 'mean_z', filename = main_label, n_files = files, labels = labels, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(parameter = 'mean_dE', filename = main_label, n_files = files, labels = labels, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(parameter = 'mean_dE', filename = main_label, n_files = files, labels = labels, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(parameter = 'epsn_x', filename = main_label, n_files = files, labels = labels, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(parameter = 'epsn_x', filename = main_label, n_files = files, labels = labels, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(parameter = 'epsn_y', filename = main_label, n_files = files, labels = labels, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(parameter = 'epsn_y', filename = main_label, n_files = files, labels = labels, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(parameter = 'eps_z', filename = main_label, n_files = files, labels = labels, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(parameter = 'eps_z', filename = main_label, n_files = files, labels = labels, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(parameter = 'bunchlength', filename = main_label, n_files = files, labels = labels, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(parameter = 'bunchlength', filename = main_label, n_files = files, labels = labels, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_parameter(parameter = 'dpp_rms', filename = main_label, n_files = files, labels = labels, percentage = False, turns = turn_tot, legend_label = legend_label)
plot_parameter(parameter = 'dpp_rms', filename = main_label, n_files = files, labels = labels, percentage = True, turns = turn_tot, legend_label = legend_label)

plot_mean_of_two_parameters(parameter1 = 'epsn_x', parameter2 = 'epsn_y', filename = main_label, n_files = files, labels = labels, legend_label = legend_label)
