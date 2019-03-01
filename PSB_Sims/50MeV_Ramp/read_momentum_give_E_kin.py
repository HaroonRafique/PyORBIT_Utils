import matplotlib.pyplot as plt
import numpy as np
import sys
from scipy.constants import speed_of_light

time_in = []
time_out = []
momentum_in = []
kinetic_energy_out = []
kinetic_energy_out_GeV = []

m_p = 938.272046E6

file_in ='momentum_program_50MeV_1.4GeV.txt'
verbose = 1

fin1=open(file_in,'r').readlines()[1:]

# Read Data
for l in fin1:  
    time_in.append(float(l.split()[0]))
    momentum_in.append(float(l.split()[1]))
    
for i in range(0, len(time_in), 1):
	time_out.append(time_in[i] - time_in[0])
	# We have p = beta * gamma * m_p * c
	# We want E_kin	
	
	# Total energy
	E_rel = np.sqrt(momentum_in[i]**2 + m_p**2)
	E_kin = E_rel - m_p
	
	# Find gamma
	gamma = E_rel / m_p
	beta = np.sqrt( 1 - (1/gamma)**2 )
	
	kinetic_energy_out.append(E_kin)
	kinetic_energy_out_GeV.append(E_kin/1E9)
	
	if verbose:
		print '\n'
		print 'Momentum = ', momentum_in[i]/1E6, 'MeV'
		print 'E_rel = ', E_rel/1E6, ' MeV'
		print 'E_kin = ', E_kin/1E6, 'MeV'
		print 'gamma = ', gamma
		print 'beta = ', beta
		
fileout = open('E_kin.txt','w') 
 
for i in range(len(time_out)): 
	fileout.write(str(time_out[i]))
	fileout.write('\t') 
	fileout.write(str(kinetic_energy_out[i]))
	fileout.write('\n') 
 
fileout.close() 

print time_out

print kinetic_energy_out_GeV

