# Plots all available plottable data from output.mat as individual files
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio 

# Function takes:
# parameter name; e.g. 'bunch_length'
# title for plot; e.g. 'Bunch Length'
# filename; e.g. 'PS_Injection' = PS_Injection_bunch_length.png
# x and y limits (default is auto)
# Can set y limits individually but not x for some strange reason
# y label; e.g. 'Bunch Length [m]'
# percentage - switch used to plot raw or percentage change from initial value

def plot_parameter(parameter, filename, title=None, ylab=None, yunit='-', ymin=None, ymax=None, percentage = False, turns = None):

	labels = ['6.07', '6.09', '6.11', '6.13', '6.15', '6.17', '6.19', '6.21']
	
	if percentage:
		print '\nPlotting ', parameter, ' percentage'
	else:
		print '\nPlotting ', parameter

	fig1 = plt.figure(figsize=(6,4))
	ax1 = fig1.add_subplot(111)
			
	if ylab is None:
		ylab = parameter
		
	if title is None:
		title = parameter
		
	if percentage:
		ax1.plot(particles_1['turn'][0], ((particles_1[parameter][0]/particles_1[parameter][0][0])*100)-100, label=labels[0]);
		ax1.plot(particles_2['turn'][0], ((particles_2[parameter][0]/particles_2[parameter][0][0])*100)-100, label=labels[1]);
		ax1.plot(particles_3['turn'][0], ((particles_3[parameter][0]/particles_3[parameter][0][0])*100)-100, label=labels[2]);
		ax1.plot(particles_4['turn'][0], ((particles_4[parameter][0]/particles_4[parameter][0][0])*100)-100, label=labels[3]);
		ax1.plot(particles_5['turn'][0], ((particles_5[parameter][0]/particles_5[parameter][0][0])*100)-100, label=labels[4]);
		ax1.plot(particles_6['turn'][0], ((particles_6[parameter][0]/particles_6[parameter][0][0])*100)-100, label=labels[5]);
		ax1.plot(particles_7['turn'][0], ((particles_7[parameter][0]/particles_7[parameter][0][0])*100)-100, label=labels[6]);
		ax1.plot(particles_8['turn'][0], ((particles_8[parameter][0]/particles_8[parameter][0][0])*100)-100, label=labels[7]);
		ylabel = str(parameter + ' percentage change [%]')
		ax1.set_ylabel(ylabel);
		figname = filename + '_' + parameter + '_percentage_nodes.png'

	else:
		ax1.plot(particles_1['turn'][0], particles_1[parameter][0], label=labels[0]);
		ax1.plot(particles_2['turn'][0], particles_2[parameter][0], label=labels[1]);
		ax1.plot(particles_3['turn'][0], particles_3[parameter][0], label=labels[2]);
		ax1.plot(particles_4['turn'][0], particles_4[parameter][0], label=labels[3]);
		ax1.plot(particles_5['turn'][0], particles_5[parameter][0], label=labels[4]);
		ax1.plot(particles_6['turn'][0], particles_6[parameter][0], label=labels[5]);
		ax1.plot(particles_7['turn'][0], particles_7[parameter][0], label=labels[6]);
		ax1.plot(particles_8['turn'][0], particles_8[parameter][0], label=labels[7]);
		ylabel = str( parameter + ' [' + yunit + ']')
		ax1.set_ylabel(ylabel);
		figname = filename + '_' + parameter + '_nodes.png'
	
	if ymin is not None:
		ax1.set_ylim(bottom = ymin)	
	if ymax is not None:
		ax1.set_ylim(top = ymax)
		
	if turns is not None: 
		ax1.set_xlim(left = 0)
		ax1.set_xlim(right = turns)
	
	ax1.legend()
	ax1.set_xlabel('Turn [-]');
	ax1.set_title(title);
	ax1.grid(True);
	
	fig1.savefig(figname);	
	return;

def plot_mean_of_two_parameters(parameter1, parameter2, filename, title=None, ylab=None, yunit='-', ymin=None, ymax=None, turns = None):

	print '\nPlotting mean of ', parameter1, 'and', parameter2,
		
	fig1 = plt.figure(figsize=(6,4))
	ax1 = fig1.add_subplot(111)
	
	labels = ['6.07', '6.09', '6.11', '6.13', '6.15', '6.17', '6.19', '6.21']
			
	if ylab is None:
		ylab = 'mean of ' + parameter1 + ' and ' + parameter2
		
	if title is None:
		title = 'mean of ' + parameter1 + ' and ' + parameter2

	ax1.plot(particles_1['turn'][0], (particles_1[parameter1][0] + particles_1[parameter2][0])/2, label=labels[0]);
	ax1.plot(particles_2['turn'][0], (particles_2[parameter1][0] + particles_2[parameter2][0])/2, label=labels[1]);
	ax1.plot(particles_3['turn'][0], (particles_3[parameter1][0] + particles_3[parameter2][0])/2, label=labels[2]);
	ax1.plot(particles_4['turn'][0], (particles_4[parameter1][0] + particles_4[parameter2][0])/2, label=labels[3]);
	ax1.plot(particles_5['turn'][0], (particles_5[parameter1][0] + particles_5[parameter2][0])/2, label=labels[4]);
	ax1.plot(particles_5['turn'][0], (particles_6[parameter1][0] + particles_6[parameter2][0])/2, label=labels[5]);
	ax1.plot(particles_5['turn'][0], (particles_7[parameter1][0] + particles_7[parameter2][0])/2, label=labels[6]);
	ax1.plot(particles_5['turn'][0], (particles_8[parameter1][0] + particles_8[parameter2][0])/2, label=labels[7]);
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
		
	ax1.legend()
	ax1.set_xlabel('Turn [-]');
	ax1.set_title(title);
	ax1.grid(True);
	
	fig1.savefig(figname);	
	return;

plt.rcParams['figure.figsize'] = [8.0, 6.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.rcParams['font.size'] = 6
plt.rcParams['legend.fontsize'] = 'small'

plt.rcParams['lines.linewidth'] = 0.5

############################
# Open files and read data #
############################

# Open File
file_1='07/output/output.mat'
file_2='09/output/output.mat'
file_3='11/output/output.mat'
file_4='13/output/output.mat'
file_5='15/output/output.mat'
file_6='17/output/output.mat'
file_7='19/output/output.mat'
file_8='21/output/output.mat'

particles_1=dict()
particles_2=dict()
particles_3=dict()
particles_4=dict()
particles_5=dict()
particles_6=dict()
particles_7=dict()
particles_8=dict()

sio.loadmat(file_1, mdict=particles_1)
sio.loadmat(file_2, mdict=particles_2)
sio.loadmat(file_3, mdict=particles_3)
sio.loadmat(file_4, mdict=particles_4)
sio.loadmat(file_5, mdict=particles_5)
sio.loadmat(file_6, mdict=particles_6)
sio.loadmat(file_7, mdict=particles_7)
sio.loadmat(file_8, mdict=particles_8)

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

turn_tot = 10000

plot_parameter(parameter = 'intensity', filename ='PS_Injection', yunit = 'protons', percentage = False, turns = turn_tot)
plot_parameter(parameter = 'intensity', filename ='PS_Injection', yunit = 'protons', percentage = True, turns = turn_tot)

plot_parameter(parameter = 'mean_x', filename ='PS_Injection', yunit = 'm', percentage = False, turns = turn_tot)
plot_parameter(parameter = 'mean_x', filename ='PS_Injection', yunit = 'm', percentage = True, turns = turn_tot)

plot_parameter(parameter = 'mean_xp', filename ='PS_Injection', yunit = 'rad', percentage = False, turns = turn_tot)
plot_parameter(parameter = 'mean_xp', filename ='PS_Injection', yunit = 'rad', percentage = True, turns = turn_tot)

plot_parameter(parameter = 'mean_y', filename ='PS_Injection', yunit = 'm', percentage = False, turns = turn_tot)
plot_parameter(parameter = 'mean_y', filename ='PS_Injection', yunit = 'm', percentage = True, turns = turn_tot)

plot_parameter(parameter = 'mean_yp', filename ='PS_Injection', yunit = 'rad', percentage = False, turns = turn_tot)
plot_parameter(parameter = 'mean_yp', filename ='PS_Injection', yunit = 'rad', percentage = True, turns = turn_tot)

plot_parameter(parameter = 'mean_z', filename ='PS_Injection', yunit = 'm', percentage = False, turns = turn_tot)
plot_parameter(parameter = 'mean_z', filename ='PS_Injection', yunit = 'm', percentage = True, turns = turn_tot)

plot_parameter(parameter = 'mean_dE', filename ='PS_Injection', yunit = 'GeV', percentage = False, turns = turn_tot)
plot_parameter(parameter = 'mean_dE', filename ='PS_Injection', yunit = 'GeV', percentage = True, turns = turn_tot)

plot_parameter(parameter = 'epsn_x', filename ='PS_Injection', yunit = 'm rad', percentage = False, turns = turn_tot)
plot_parameter(parameter = 'epsn_x', filename ='PS_Injection', yunit = 'm rad', percentage = True, turns = turn_tot)

plot_parameter(parameter = 'epsn_y', filename ='PS_Injection', yunit = 'm rad', percentage = False, turns = turn_tot)
plot_parameter(parameter = 'epsn_y', filename ='PS_Injection', yunit = 'm rad', percentage = True, turns = turn_tot)

plot_parameter(parameter = 'eps_z', filename ='PS_Injection', yunit = 'eV s', percentage = False, turns = turn_tot)
plot_parameter(parameter = 'eps_z', filename ='PS_Injection', yunit = 'eV s', percentage = True, turns = turn_tot)

plot_parameter(parameter = 'bunchlength', filename ='PS_Injection', yunit = 'm', percentage = False, turns = turn_tot)
plot_parameter(parameter = 'bunchlength', filename ='PS_Injection', yunit = 'm', percentage = True, turns = turn_tot)

plot_parameter(parameter = 'dpp_rms', filename ='PS_Injection', yunit = '-', percentage = False, turns = turn_tot)
plot_parameter(parameter = 'dpp_rms', filename ='PS_Injection', yunit = '-', percentage = True, turns = turn_tot)

plot_mean_of_two_parameters(parameter1 = 'epsn_x', parameter2 = 'epsn_y', filename ='PS_Injection', yunit = 'm rad')
