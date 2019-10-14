#!/usr/bin/python
# Python script to copy various outputs from HPC-Batch to SWAN (EOS)
import os

print '\nSTARTED copy_outputs_to_EOS.py'

case = 'V_Scan_Fixed_Bump'
case_short = 'VB'

def make_output_copy_command(loc, case, case_short):
	return 'cp output.mat /afs/cern.ch/user/h/harafiqu/EOS/SWAN_projects/PS/From_Scratch/Simulation_Output/'+ str(case) + '/Outputs' + str(loc) + '_' + str(case_short) + '_output.mat'

def make_bunch_copy_commands(loc, case):
	return ['cp mainbunch_000874.mat /afs/cern.ch/user/h/harafiqu/EOS/SWAN_projects/PS/From_Scratch/Simulation_Output/'+ str(case) + '/Bunch_Profiles' + str(loc) + '_c172.mat', 'cp mainbunch_002185.mat /afs/cern.ch/user/h/harafiqu/EOS/SWAN_projects/PS/From_Scratch/Simulation_Output/'+ str(case) + '/Bunch_Profiles' + str(loc) + '_c175.mat']

# Present directory
master_dir = os.getcwd()

sbs_locations = []

#sbs_locations.append('/610_SbS')
#sbs_locations.append('/611_SbS')
sbs_locations.append('/612_SbS')
sbs_locations.append('/613_SbS')
sbs_locations.append('/614_SbS')
sbs_locations.append('/615_SbS')
sbs_locations.append('/616_SbS')
sbs_locations.append('/617_SbS')
sbs_locations.append('/618_SbS')
sbs_locations.append('/619_SbS')
sbs_locations.append('/620_SbS')
sbs_locations.append('/621_SbS')
sbs_locations.append('/622_SbS')
sbs_locations.append('/623_SbS')
sbs_locations.append('/624_SbS')

for loc in sbs_locations:
	print '\nStarted loop for folder', loc
	
	# Create a full path to output folder
	out_dir = master_dir + loc + '/PyORBIT/output'
	print '\n\tcd ', out_dir

	# change directory to output folder
	os.chdir(out_dir)

	# copy output file with correct naming convention
	print '\n\t' + str(make_output_copy_command(loc, case, case_short))
	os.system(make_output_copy_command(loc, case, case_short))
	
	# change directory to bunch output folder
	bunch_dir = master_dir + loc + '/PyORBIT/bunch_output'
	print '\n\tcd ', bunch_dir
	os.chdir(bunch_dir)
	
	# copy output files with correct naming convention
	comm_172, comm_175= make_bunch_copy_commands(loc, case)
	print '\n\t' + str(comm_172)
	os.system(comm_172)
	print '\n\t' + str(comm_175)
	os.system(comm_175)
	
	print '\nFinished loop for folder\n', loc

print '\nFINISHED copy_outputs_to_EOS.py'
