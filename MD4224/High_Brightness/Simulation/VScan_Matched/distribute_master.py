import shutil

pyorbit = False
simulation_parameters = True
flat_files = False

sbs = False
noSC = True

master_directory = './Master'
pyorbit_file = master_directory + '/pyOrbit.py'
sim_params_file = master_directory + '/simulation_parameters.py'
flat_file = master_directory + '/Flat_file.madx'

sbs_locations = []
noSC_locations = []

sbs_locations.append('./610_SbS/')
sbs_locations.append('./611_SbS/')
sbs_locations.append('./612_SbS/')
sbs_locations.append('./613_SbS/')
sbs_locations.append('./614_SbS/')
sbs_locations.append('./615_SbS/')
sbs_locations.append('./616_SbS/')
sbs_locations.append('./617_SbS/')
sbs_locations.append('./618_SbS/')
sbs_locations.append('./619_SbS/')
sbs_locations.append('./620_SbS/')
sbs_locations.append('./621_SbS/')
sbs_locations.append('./622_SbS/')
sbs_locations.append('./623_SbS/')
sbs_locations.append('./624_SbS/')

noSC_locations.append('./624_noSC/')
noSC_locations.append('./622_noSC/')
noSC_locations.append('./620_noSC/')
noSC_locations.append('./618_noSC/')
noSC_locations.append('./616_noSC/')
noSC_locations.append('./614_noSC/')
noSC_locations.append('./612_noSC/')
noSC_locations.append('./610_noSC/')

if pyorbit:
	if sbs:
		for loc in sbs_locations:
			newPath = shutil.copy(pyorbit_file, loc)
			print pyorbit_file, ' copied to ', loc
	if noSC:
		for loc in noSC_locations:
			newPath = shutil.copy(pyorbit_file, loc)
			print pyorbit_file, ' copied to ', loc

if simulation_parameters:
	if sbs:
		for loc in sbs_locations:
			newPath = shutil.copy(sim_params_file, loc)
			print sim_params_file, ' copied to ', loc
	if noSC:
		for loc in noSC_locations:
			newPath = shutil.copy(sim_params_file, loc)
			print sim_params_file, ' copied to ', loc

if flat_files:
	if sbs:
		for loc in sbs_locations:
			newPath = shutil.copy(flat_file, loc)
			print flat_file, ' copied to ', loc
	if noSC:
		for loc in noSC_locations:
			newPath = shutil.copy(flat_file, loc)
			print flat_file, ' copied to ', loc
