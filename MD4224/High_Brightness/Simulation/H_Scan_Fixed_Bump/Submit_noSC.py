import os

sbs = True

master_dir = os.getcwd()

sbs_locations = []

sbs_locations.append('/607_noSC/PyORBIT')
sbs_locations.append('/609_noSC/PyORBIT')
sbs_locations.append('/611_noSC/PyORBIT')
sbs_locations.append('/613_noSC/PyORBIT')
sbs_locations.append('/615_noSC/PyORBIT')
sbs_locations.append('/617_noSC/PyORBIT')
sbs_locations.append('/619_noSC/PyORBIT')
sbs_locations.append('/621_noSC/PyORBIT')

if sbs:
	for loc in sbs_locations:
		dir_ = master_dir + loc
		make_command = 'python Make_SLURM_submission_script.py'		
		submit_command = 'sbatch SLURM_submission_script.sh'
		os.chdir(dir_)
		os.system(make_command)		
		os.system(submit_command)
