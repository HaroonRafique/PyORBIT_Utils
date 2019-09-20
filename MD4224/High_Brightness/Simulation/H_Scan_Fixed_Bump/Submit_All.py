import os

sbs = True

master_dir = os.getcwd()

sbs_locations = []

sbs_locations.append('/607_SbS/PyORBIT')
sbs_locations.append('/608_SbS/PyORBIT')
sbs_locations.append('/609_SbS/PyORBIT')
sbs_locations.append('/610_SbS/PyORBIT')
sbs_locations.append('/611_SbS/PyORBIT')
sbs_locations.append('/612_SbS/PyORBIT')
sbs_locations.append('/613_SbS/PyORBIT')
sbs_locations.append('/614_SbS/PyORBIT')
sbs_locations.append('/615_SbS/PyORBIT')
sbs_locations.append('/616_SbS/PyORBIT')
sbs_locations.append('/617_SbS/PyORBIT')
sbs_locations.append('/618_SbS/PyORBIT')
sbs_locations.append('/619_SbS/PyORBIT')
sbs_locations.append('/620_SbS/PyORBIT')
sbs_locations.append('/621_SbS/PyORBIT')

if sbs:
	for loc in sbs_locations:
		dir_ = master_dir + loc
		make_command = 'python Make_SLURM_submission_script.py'
		submit_command = 'sbatch SLURM_submission_script.sh'
		os.chdir(dir_)
		os.system(make_command)
		os.system(submit_command)
