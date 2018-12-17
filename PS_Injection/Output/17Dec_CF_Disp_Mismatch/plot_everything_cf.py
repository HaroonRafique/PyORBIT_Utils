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

def plot_parameter(parameter, filename, title=None, ylab=None, yunit='-', ymin=None, ymax=None, percentage = False):

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
		ax1.plot(particles_1p3['turn'][0], ((particles_1p3[parameter][0]/particles_1p3[parameter][0][0])*100)-100, label='1.3 eVs');
		ax1.plot(particles_1p6['turn'][0], ((particles_1p6[parameter][0]/particles_1p6[parameter][0][0])*100)-100, label='1.6 eVs');
		ax1.plot(particles_1p9['turn'][0], ((particles_1p9[parameter][0]/particles_1p9[parameter][0][0])*100)-100, label='1.9 eVs');
		ax1.plot(particles_2p3['turn'][0], ((particles_2p3[parameter][0]/particles_2p3[parameter][0][0])*100)-100, label='2.3 eVs');
		ax1.plot(particles_2p6['turn'][0], ((particles_2p6[parameter][0]/particles_2p6[parameter][0][0])*100)-100, label='2.6 eVs');
		ylabel = str(parameter + ' percentage change [%]')
		ax1.set_ylabel(ylabel);
		figname = filename + '_' + parameter + '_percentage_nodes.png'

	else:
		ax1.plot(particles_1p3['turn'][0], particles_1p3[parameter][0], label='1.3 eVs');
		ax1.plot(particles_1p6['turn'][0], particles_1p6[parameter][0], label='1.6 eVs');
		ax1.plot(particles_1p9['turn'][0], particles_1p9[parameter][0], label='1.9 eVs');
		ax1.plot(particles_2p3['turn'][0], particles_2p3[parameter][0], label='2.3 eVs');
		ax1.plot(particles_2p6['turn'][0], particles_2p6[parameter][0], label='2.6 eVs');
		ylabel = str( parameter + ' [' + yunit + ']')
		ax1.set_ylabel(ylabel);
		figname = filename + '_' + parameter + '_nodes.png'
	
	if ymin is not None:
		ax1.set_ylim(bottom = ymin)	
	if ymax is not None:
		ax1.set_ylim(top = ymax)
	
	ax1.legend()
	ax1.set_xlabel('Turn [-]');
	ax1.set_title(title);
	ax1.grid(True);
	
	fig1.savefig(figname);	
	return;

def plot_parameter_cf(parameter, filename, label1, label2, title=None, ylab=None, yunit='-', ymin=None, ymax=None, percentage = False):

	if percentage:
		print '\nPlotting ', parameter, ' percentage comparison'
	else:
		print '\nPlotting ', parameter, 'comparison'

	fig1 = plt.figure(figsize=(6,4))
	ax1 = fig1.add_subplot(111)
			
	if ylab is None:
		ylab = parameter
		
	if title is None:
		title = parameter
		
	if percentage:
		ax1.plot(particles_1p3['turn'][0], ((particles_1p3[parameter][0]/particles_1p3[parameter][0][0])*100)-100, 'b', label=('1.3 eVs '+label1));
		ax1.plot(particles_1p6['turn'][0], ((particles_1p6[parameter][0]/particles_1p6[parameter][0][0])*100)-100, 'g', label=('1.6 eVs '+label1));
		ax1.plot(particles_1p9['turn'][0], ((particles_1p9[parameter][0]/particles_1p9[parameter][0][0])*100)-100, 'r', label=('1.9 eVs '+label1));
		ax1.plot(particles_2p3['turn'][0], ((particles_2p3[parameter][0]/particles_2p3[parameter][0][0])*100)-100, 'm', label=('2.3 eVs '+label1));
		ax1.plot(particles_2p6['turn'][0], ((particles_2p6[parameter][0]/particles_2p6[parameter][0][0])*100)-100, 'k', label=('2.6 eVs '+label1));
		
		ax1.plot(particles_1p3_2['turn'][0], ((particles_1p3_2[parameter][0]/particles_1p3_2[parameter][0][0])*100)-100, 'b--', label=('1.3 eVs '+label2));
		ax1.plot(particles_1p6_2['turn'][0], ((particles_1p6_2[parameter][0]/particles_1p6_2[parameter][0][0])*100)-100, 'g--', label=('1.6 eVs '+label2));
		ax1.plot(particles_1p9_2['turn'][0], ((particles_1p9_2[parameter][0]/particles_1p9_2[parameter][0][0])*100)-100, 'r--', label=('1.9 eVs '+label2));
		ax1.plot(particles_2p3_2['turn'][0], ((particles_2p3_2[parameter][0]/particles_2p3_2[parameter][0][0])*100)-100, 'm--', label=('2.3 eVs '+label2));
		ax1.plot(particles_2p6_2['turn'][0], ((particles_2p6_2[parameter][0]/particles_2p6_2[parameter][0][0])*100)-100, 'k--', label=('2.6 eVs '+label2));
		
		ylabel = str(parameter + ' percentage change [%]')
		ax1.set_ylabel(ylabel);
		figname = filename + '_' + parameter + '_percentage_cf_' + label1 + '_' + label2 + '.png'

	else:
		ax1.plot(particles_1p3['turn'][0], particles_1p3[parameter][0], 'b', label=('1.3 eVs '+label1));
		ax1.plot(particles_1p6['turn'][0], particles_1p6[parameter][0], 'g', label=('1.6 eVs '+label1));
		ax1.plot(particles_1p9['turn'][0], particles_1p9[parameter][0], 'r', label=('1.9 eVs '+label1));
		ax1.plot(particles_2p3['turn'][0], particles_2p3[parameter][0], 'm', label=('2.3 eVs '+label1));
		ax1.plot(particles_2p6['turn'][0], particles_2p6[parameter][0], 'k', label=('2.6 eVs '+label1));
		
		ax1.plot(particles_1p3_2['turn'][0], particles_1p3_2[parameter][0], 'b--', label=('1.3 eVs '+label2));
		ax1.plot(particles_1p6_2['turn'][0], particles_1p6_2[parameter][0], 'g--', label=('1.6 eVs '+label2));
		ax1.plot(particles_1p9_2['turn'][0], particles_1p9_2[parameter][0], 'r--', label=('1.9 eVs '+label2));
		ax1.plot(particles_2p3_2['turn'][0], particles_2p3_2[parameter][0], 'm--', label=('2.3 eVs '+label2));
		ax1.plot(particles_2p6_2['turn'][0], particles_2p6_2[parameter][0], 'k--', label=('2.6 eVs '+label2));
		
		ylabel = str( parameter + ' [' + yunit + ']')
		ax1.set_ylabel(ylabel);
		figname = filename + '_' + parameter + '_nodes_cf_' + label1 + '_' + label2 + '.png'
	
	if ymin is not None:
		ax1.set_ylim(bottom = ymin)	
	if ymax is not None:
		ax1.set_ylim(top = ymax)		
	
	#ax1.set_xlim(0, 1000)
	
	ax1.legend()
	ax1.set_xlabel('Turn [-]');
	ax1.set_title(title);
	ax1.grid(True);
	
	fig1.savefig(figname);	
	return;

def plot_mean_of_two_parameters(parameter1, parameter2, filename, title=None, ylab=None, yunit='-', ymin=None, ymax=None):

	print '\nPlotting mean of ', parameter1, 'and', parameter2,
		
	fig1 = plt.figure(figsize=(6,4))
	ax1 = fig1.add_subplot(111)
			
	if ylab is None:
		ylab = 'mean of ' + parameter1 + ' and ' + parameter2
		
	if title is None:
		title = 'mean of ' + parameter1 + ' and ' + parameter2

	ax1.plot(particles_1p3['turn'][0], (particles_1p3[parameter1][0] + particles_1p3[parameter2][0])/2, label='1.3 eVs');
	ax1.plot(particles_1p6['turn'][0], (particles_1p6[parameter1][0] + particles_1p6[parameter2][0])/2, label='1.6 eVs');
	ax1.plot(particles_1p9['turn'][0], (particles_1p9[parameter1][0] + particles_1p9[parameter2][0])/2, label='1.9 eVs');
	ax1.plot(particles_2p3['turn'][0], (particles_2p3[parameter1][0] + particles_2p3[parameter2][0])/2, label='2.3 eVs');
	ax1.plot(particles_2p6['turn'][0], (particles_2p6[parameter1][0] + particles_2p6[parameter2][0])/2, label='2.6 eVs');
	ylabel = str( 'mean of ' + parameter1 + ' and ' + parameter2 + ' [' + yunit + ']')
	ax1.set_ylabel(ylabel);
	figname = filename + '_mean_of_' + parameter1 + '_' + parameter2 + '_nodes.png'
	
	if ymin is not None:
		ax1.set_ylim(bottom = ymin)	
	if ymax is not None:
		ax1.set_ylim(top = ymax)
	
	ax1.legend()
	ax1.set_xlabel('Turn [-]');
	ax1.set_title(title);
	ax1.grid(True);
	
	fig1.savefig(figname);	
	return;
	
	
def plot_mean_of_two_parameters_cf(parameter1, parameter2, filename, label1, label2, title=None, ylab=None, yunit='-', ymin=None, ymax=None):

	print '\nPlotting mean of ', parameter1, 'and', parameter2,
		
	fig1 = plt.figure(figsize=(6,4))
	ax1 = fig1.add_subplot(111)
			
	if ylab is None:
		ylab = 'mean of ' + parameter1 + ' and ' + parameter2
		
	if title is None:
		title = 'mean of ' + parameter1 + ' and ' + parameter2

	ax1.plot(particles_1p3['turn'][0], (particles_1p3[parameter1][0] + particles_1p3[parameter2][0])/2, 'b', label='1.3 eVs');
	ax1.plot(particles_1p6['turn'][0], (particles_1p6[parameter1][0] + particles_1p6[parameter2][0])/2, 'g', label='1.6 eVs');
	ax1.plot(particles_1p9['turn'][0], (particles_1p9[parameter1][0] + particles_1p9[parameter2][0])/2, 'r', label='1.9 eVs');
	ax1.plot(particles_2p3['turn'][0], (particles_2p3[parameter1][0] + particles_2p3[parameter2][0])/2, 'm', label='2.3 eVs');
	ax1.plot(particles_2p6['turn'][0], (particles_2p6[parameter1][0] + particles_2p6[parameter2][0])/2, 'k', label='2.6 eVs');
	
	
	ax1.plot(particles_1p3_2['turn'][0], (particles_1p3_2[parameter1][0] + particles_1p3_2[parameter2][0])/2, 'b--', label='1.3 eVs');
	ax1.plot(particles_1p6_2['turn'][0], (particles_1p6_2[parameter1][0] + particles_1p6_2[parameter2][0])/2, 'g--', label='1.6 eVs');
	ax1.plot(particles_1p9_2['turn'][0], (particles_1p9_2[parameter1][0] + particles_1p9_2[parameter2][0])/2, 'r--', label='1.9 eVs');
	ax1.plot(particles_2p3_2['turn'][0], (particles_2p3_2[parameter1][0] + particles_2p3_2[parameter2][0])/2, 'm--', label='2.3 eVs');
	ax1.plot(particles_2p6_2['turn'][0], (particles_2p6_2[parameter1][0] + particles_2p6_2[parameter2][0])/2, 'k--', label='2.6 eVs');
	
	ylabel = str( 'mean of ' + parameter1 + ' and ' + parameter2 + ' [' + yunit + ']')
	ax1.set_ylabel(ylabel);
	figname = filename + '_mean_of_' + parameter1 + '_' + parameter2 + '_nodes.png'
	
	if ymin is not None:
		ax1.set_ylim(bottom = ymin)	
	if ymax is not None:
		ax1.set_ylim(top = ymax)
	
	#ax1.set_xlim(0, 1000)
	
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
file_1p3='/home/HR/Documents/PyORBIT_Utils/PS_Injection/Output/17Oct18_New_Params/I=2.0/output/output_1p3.mat'
file_1p6='/home/HR/Documents/PyORBIT_Utils/PS_Injection/Output/17Oct18_New_Params/I=2.0/output/output_1p6.mat'
file_1p9='/home/HR/Documents/PyORBIT_Utils/PS_Injection/Output/17Oct18_New_Params/I=2.0/output/output_1p9.mat'
file_2p3='/home/HR/Documents/PyORBIT_Utils/PS_Injection/Output/17Oct18_New_Params/I=2.0/output/output_2p3.mat'
file_2p6='/home/HR/Documents/PyORBIT_Utils/PS_Injection/Output/17Oct18_New_Params/I=2.0/output/output_2p6.mat'

file_1p3_2='/home/HR/Documents/PyORBIT_Utils/PS_Injection/Output/14Dec18_Dispersion_Mismatch_1p3/output/output_1p3.mat'
file_1p6_2='/home/HR/Documents/PyORBIT_Utils/PS_Injection/Output/14Dec18_Dispersion_Mismatch_1p3/output/output_1p6.mat'
file_1p9_2='/home/HR/Documents/PyORBIT_Utils/PS_Injection/Output/14Dec18_Dispersion_Mismatch_1p3/output/output_1p9.mat'
file_2p3_2='/home/HR/Documents/PyORBIT_Utils/PS_Injection/Output/14Dec18_Dispersion_Mismatch_1p3/output/output_2p3.mat'
file_2p6_2='/home/HR/Documents/PyORBIT_Utils/PS_Injection/Output/14Dec18_Dispersion_Mismatch_1p3/output/output_2p6.mat'

lab1 = 'Original'
lab2 = 'D_Mismatch_1p3'
#fname = 'PS_Injection_Nt=1000'
fname = 'PS_Injection'

particles_1p3=dict()
particles_1p6=dict()
particles_1p9=dict()
particles_2p3=dict()
particles_2p6=dict()

particles_1p3_2=dict()
particles_1p6_2=dict()
particles_1p9_2=dict()
particles_2p3_2=dict()
particles_2p6_2=dict()

sio.loadmat(file_1p3, mdict=particles_1p3)
sio.loadmat(file_1p6, mdict=particles_1p6)
sio.loadmat(file_1p9, mdict=particles_1p9)
sio.loadmat(file_2p3, mdict=particles_2p3)
sio.loadmat(file_2p6, mdict=particles_2p6)

sio.loadmat(file_1p3_2, mdict=particles_1p3_2)
sio.loadmat(file_1p6_2, mdict=particles_1p6_2)
sio.loadmat(file_1p9_2, mdict=particles_1p9_2)
sio.loadmat(file_2p3_2, mdict=particles_2p3_2)
sio.loadmat(file_2p6_2, mdict=particles_2p6_2)

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

plot_parameter_cf(parameter = 'intensity', filename =fname, label1 = lab1, label2 = lab2, yunit = 'protons', percentage = False)
plot_parameter_cf(parameter = 'intensity', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'protons', percentage = True)

plot_parameter_cf(parameter = 'mean_x', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'm', percentage = False)
plot_parameter_cf(parameter = 'mean_x', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'm', percentage = True)

plot_parameter_cf(parameter = 'mean_xp', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'rad', percentage = False)
plot_parameter_cf(parameter = 'mean_xp', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'rad', percentage = True)

plot_parameter_cf(parameter = 'mean_y', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'm', percentage = False)
plot_parameter_cf(parameter = 'mean_y', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'm', percentage = True)

plot_parameter_cf(parameter = 'mean_yp', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'rad', percentage = False)
plot_parameter_cf(parameter = 'mean_yp', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'rad', percentage = True)

plot_parameter_cf(parameter = 'mean_z', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'm', percentage = False)
plot_parameter_cf(parameter = 'mean_z', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'm', percentage = True)

plot_parameter_cf(parameter = 'mean_dE', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'GeV', percentage = False)
plot_parameter_cf(parameter = 'mean_dE', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'GeV', percentage = True)

plot_parameter_cf(parameter = 'epsn_x', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'm rad', percentage = False)
plot_parameter_cf(parameter = 'epsn_x', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'm rad', percentage = True)

plot_parameter_cf(parameter = 'epsn_y', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'm rad', percentage = False)
plot_parameter_cf(parameter = 'epsn_y', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'm rad', percentage = True)

plot_parameter_cf(parameter = 'eps_z', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'eV s', percentage = False)
plot_parameter_cf(parameter = 'eps_z', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'eV s', percentage = True)

plot_parameter_cf(parameter = 'bunchlength', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'm', percentage = False)
plot_parameter_cf(parameter = 'bunchlength', filename =fname, label1 = lab1, label2 = lab2,  yunit = 'm', percentage = True)

plot_parameter_cf(parameter = 'dpp_rms', filename =fname, label1 = lab1, label2 = lab2,  yunit = '-', percentage = False)
plot_parameter_cf(parameter = 'dpp_rms', filename =fname, label1 = lab1, label2 = lab2,  yunit = '-', percentage = True)

plot_mean_of_two_parameters_cf(parameter1 = 'epsn_x', parameter2 = 'epsn_y', filename =fname, label1 = lab1, label2 = lab2, yunit = 'm rad')
