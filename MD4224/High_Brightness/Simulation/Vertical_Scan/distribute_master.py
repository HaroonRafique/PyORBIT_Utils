import shutil

sbs = False
sbs_nolk = True
twopfive = False

master_directory = './Master'
pyorbit_file = master_directory + '/pyOrbit.py'
sim_params_file = master_directory + '/simulation_parameters.py'

sbs_locations = []
twopfive_locations = []
sbs_nlk_locations = []

sbs_locations.append('./610_SbS/')
sbs_locations.append('./612_SbS/')
sbs_locations.append('./614_SbS/')
sbs_locations.append('./616_SbS/')
sbs_locations.append('./618_SbS/')
sbs_locations.append('./620_SbS/')
sbs_locations.append('./622_SbS/')
sbs_locations.append('./624_SbS/')

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

if sbs:
	for loc in sbs_locations:
		newPath = shutil.copy(pyorbit_file, loc)
		newPath = shutil.copy(sim_params_file, loc)
		print pyorbit_file, ' copied to ', loc
if sbs_nolk:
	for loc in sbs_nlk_locations:
		newPath = shutil.copy(pyorbit_file, loc)
		newPath = shutil.copy(sim_params_file, loc)
		print pyorbit_file, ' copied to ', loc
if twopfive:
	for loc in twopfive_locations:
		newPath = shutil.copy(pyorbit_file, loc)
		newPath = shutil.copy(sim_params_file, loc)
		print pyorbit_file, ' copied to ', loc
