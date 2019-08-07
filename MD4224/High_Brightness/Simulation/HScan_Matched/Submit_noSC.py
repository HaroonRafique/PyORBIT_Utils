import os

sbs = True

master_dir = os.getcwd()

sbs_locations = []

sbs_locations.append('/607_noSC')
# ~ sbs_locations.append('/608_noSC')
sbs_locations.append('/609_noSC')
# ~ sbs_locations.append('/610_noSC')
sbs_locations.append('/611_noSC')
# ~ sbs_locations.append('/612_noSC')
sbs_locations.append('/613_noSC')
# ~ sbs_locations.append('/614_noSC')
sbs_locations.append('/615_noSC')
# ~ sbs_locations.append('/616_noSC')
sbs_locations.append('/617_noSC')
# ~ sbs_locations.append('/618_noSC')
sbs_locations.append('/619_noSC')
# ~ sbs_locations.append('/620_noSC')
sbs_locations.append('/621_noSC')

if sbs:
	for loc in sbs_locations:
		dir_ = master_dir + loc
		make_command = 'python Make_SLURM_submission_script.py'		
		submit_command = 'sbatch SLURM_submission_script.sh'
		os.chdir(dir_)
		os.system(make_command)		
		os.system(submit_command)
