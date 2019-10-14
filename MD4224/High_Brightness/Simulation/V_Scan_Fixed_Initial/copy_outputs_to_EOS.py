#!/usr/bin/python
# Python script to copy various outputs from HPC-Batch to SWAN (EOS)
import os

case = 'V_Scan_Fixed_Initial'
case_short = 'VF'

cp output.mat /afs/cern.ch/user/h/harafiqu/EOS/SWAN_projects/PS/From_Scratch/Simulation_Output/V_Scan_Fixed_Initial/Outputs/610_SbS_VF_output.mat
cp mainbunch_000874.mat /afs/cern.ch/user/h/harafiqu/EOS/SWAN_projects/PS/From_Scratch/Simulation_Output/V_Scan_Fixed_Initial/Bunch_Profiles/610_SbS_c172.mat
cp mainbunch_002185.mat /afs/cern.ch/user/h/harafiqu/EOS/SWAN_projects/PS/From_Scratch/Simulation_Output/V_Scan_Fixed_Initial/Bunch_Profiles/610_SbS_c175.mat

def make_output_copy_command(loc, case, case_short):
	return 'cp output.mat /afs/cern.ch/user/h/harafiqu/EOS/SWAN_projects/PS/From_Scratch/Simulation_Output/'+ str(case) + '/Outputs/' + str(loc) + '_' + str(case_short) + '_output.mat'

def make_bunch_copy_commands(loc, case):
	return ['cp mainbunch_000874.mat /afs/cern.ch/user/h/harafiqu/EOS/SWAN_projects/PS/From_Scratch/Simulation_Output/'+ str(case) + '/Bunch_Profiles/' + str(loc) + '_c172_output.mat', 'cp mainbunch_002185.mat /afs/cern.ch/user/h/harafiqu/EOS/SWAN_projects/PS/From_Scratch/Simulation_Output/'+ str(case) + '/Bunch_Profiles/' + str(loc) + '_c175_output.mat']

# Present directory
master_dir = os.getcwd()

sbs_locations = []

# ~ sbs_locations.append('/610_SbS')
sbs_locations.append('/611_SbS')
# ~ sbs_locations.append('/612_SbS')
# ~ sbs_locations.append('/613_SbS')
# ~ sbs_locations.append('/614_SbS')
# ~ sbs_locations.append('/615_SbS')
# ~ sbs_locations.append('/616_SbS')
# ~ sbs_locations.append('/617_SbS')
# ~ sbs_locations.append('/618_SbS')
# ~ sbs_locations.append('/619_SbS')
# ~ sbs_locations.append('/620_SbS')
# ~ sbs_locations.append('/621_SbS')
# ~ sbs_locations.append('/622_SbS')
# ~ sbs_locations.append('/623_SbS')
# ~ sbs_locations.append('/624_SbS')

for loc in sbs_locations:
	# Create a full path to output folder
	out_dir = master_dir + loc + '/output'

	# change directory to output folder
	os.chdir(out_dir)

	# copy output file with correct naming convention
	os.system(make_output_copy_command(loc, case, case_short))
	
	# change directory to bunch output folder
	bunch_dir = master_dir + loc + '/bunch_output'
	os.chdir(bunch_dir)
	
	# copy output files with correct naming convention
	comm_172, comm_175= make_bunch_copy_commands(loc, case)
	os.system(comm_172)
	os.system(comm_175)
