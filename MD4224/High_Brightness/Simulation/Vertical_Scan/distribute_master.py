import shutil

pyorbit = False
simulation_parameters = False
flat_files = True

sbs = True
sbs_nolk = True
twopfive = True
no_SC = True

master_directory = './Master'
pyorbit_file = master_directory + '/pyOrbit.py'
sim_params_file = master_directory + '/simulation_parameters.py'
flat_file = master_directory + '/Flat_file.madx'

sbs_locations = []
twopfive_locations = []
sbs_nlk_locations = []
no_SC_locations = []

sbs_locations.append('./610_SbS/')
sbs_locations.append('./612_SbS/')
sbs_locations.append('./614_SbS/')
sbs_locations.append('./616_SbS/')
sbs_locations.append('./618_SbS/')
sbs_locations.append('./620_SbS/')
sbs_locations.append('./622_SbS/')
sbs_locations.append('./624_SbS/')

no_SC_locations.append('./610_noSC')
no_SC_locations.append('./612_noSC')
no_SC_locations.append('./614_noSC')
no_SC_locations.append('./616_noSC')
no_SC_locations.append('./618_noSC')
no_SC_locations.append('./620_noSC')
no_SC_locations.append('./622_noSC')
no_SC_locations.append('./624_noSC')

sbs_nlk_locations.append('./610_SbS_nLK/')
sbs_nlk_locations.append('./612_SbS_nLK/')
sbs_nlk_locations.append('./614_SbS_nLK/')
sbs_nlk_locations.append('./616_SbS_nLK/')
sbs_nlk_locations.append('./618_SbS_nLK/')
sbs_nlk_locations.append('./620_SbS_nLK/')
sbs_nlk_locations.append('./622_SbS_nLK/')
sbs_nlk_locations.append('./624_SbS_nLK/')

twopfive_locations.append('./610_2p5/')
twopfive_locations.append('./612_2p5/')
twopfive_locations.append('./614_2p5/')
twopfive_locations.append('./616_2p5/')
twopfive_locations.append('./618_2p5/')
twopfive_locations.append('./620_2p5/')
twopfive_locations.append('./622_2p5/')
twopfive_locations.append('./624_2p5/')

if pyorbit:
	if sbs:
		for loc in sbs_locations:
			newPath = shutil.copy(pyorbit_file, loc)
			print pyorbit_file, ' copied to ', loc
	if sbs_nolk:
		for loc in sbs_nlk_locations:
			newPath = shutil.copy(pyorbit_file, loc)
			print pyorbit_file, ' copied to ', loc
	if twopfive:
		for loc in twopfive_locations:
			newPath = shutil.copy(pyorbit_file, loc)
			print pyorbit_file, ' copied to ', loc
	if no_SC:
		for loc in no_SC_locations:
			newPath = shutil.copy(pyorbit_file, loc)
			print pyorbit_file, ' copied to ', loc

if simulation_parameters:
	if sbs:
		for loc in sbs_locations:
			newPath = shutil.copy(sim_params_file, loc)
			print sim_params_file, ' copied to ', loc
	if sbs_nolk:
		for loc in sbs_nlk_locations:
			newPath = shutil.copy(sim_params_file, loc)
			print sim_params_file, ' copied to ', loc
	if twopfive:
		for loc in twopfive_locations:
			newPath = shutil.copy(sim_params_file, loc)
			print sim_params_file, ' copied to ', loc
	if no_SC:
		for loc in no_SC_locations:
			newPath = shutil.copy(sim_params_file, loc)
			print sim_params_file, ' copied to ', loc

if flat_files:
	if sbs:
		for loc in sbs_locations:
			newPath = shutil.copy(flat_file, loc)
			print sim_params_file, ' copied to ', loc
	if sbs_nolk:
		for loc in sbs_nlk_locations:
			newPath = shutil.copy(flat_file, loc)
			print sim_params_file, ' copied to ', loc
	if twopfive:
		for loc in twopfive_locations:
			newPath = shutil.copy(flat_file, loc)
			print sim_params_file, ' copied to ', loc
	if no_SC:
		for loc in no_SC_locations:
			newPath = shutil.copy(flat_file, loc)
			print sim_params_file, ' copied to ', loc
