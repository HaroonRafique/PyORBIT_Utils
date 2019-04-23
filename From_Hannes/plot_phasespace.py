import os
import numpy as np
import scipy.io as sio
import pylab as plt
import glob
from lib.TuneDiagram.tune_diagram import resonance_lines


plt.close('all')

# source_dir = 'Input/'
source_dir = 'Output/'

filename = 'mainbunch'
files = glob.glob(source_dir + filename + '*.mat')
files.sort()

# particleIDreference = sio.loadmat(files[0])['particles'][0][0]['ParticleIdNumber'].flatten()
for i, file in enumerate(files[::-1]):
	print file
	try: 
		turn = int(file.split('mainbunch_')[-1][:-4])
		turn = '%04d'%turn
	except:
		turn = ''
	particles = sio.loadmat(file)['particles']
	x  = particles[0][0]['x'].flatten()
	xp = particles[0][0]['xp'].flatten()
	y  = particles[0][0]['y'].flatten()
	yp = particles[0][0]['yp'].flatten()
	z  = particles[0][0]['z'].flatten()
	dE = particles[0][0]['dE'].flatten()

	fontsize=15
	bins=500
	my_cmap = plt.cm.jet
	my_cmap.set_under('w',1)
	f, axs = plt.subplots(2,2,figsize=(10,8))
	ax = axs[0,0]
	ax.hist2d(x, xp,bins=bins, cmap=my_cmap, vmin=1)
	ax.set_xlabel('x [m]')
	ax.set_ylabel('xp ')
	ax = axs[0,1]
	ax.hist2d(y, yp,bins=bins, cmap=my_cmap, vmin=1)
	ax.set_xlabel('y [m]')
	ax.set_ylabel('yp ')
	ax = axs[1,0]
	ax.hist2d(x, y,bins=bins, cmap=my_cmap, vmin=1)
	ax.set_xlabel('x [m]')
	ax.set_ylabel('y [m] ')
	ax = axs[1,1]
	ax.hist2d(z, dE,bins=bins, cmap=my_cmap, vmin=1)
	ax.set_xlabel('z [m]')
	ax.set_ylabel('dE [GeV] ')
	for ax in axs.flatten():
		ax.xaxis.label.set_size(fontsize)
		ax.yaxis.label.set_size(fontsize)
		ax.tick_params(labelsize=fontsize)
	plt.suptitle('turn %s'%turn, fontsize=fontsize)
	plt.tight_layout(rect=[0, 0.03, 1, 0.95])
	plt.savefig('png/phasespace_%s.png'%turn, dpi=400)
	plt.close('all')
	
	qx = particles['ParticlePhaseAttributes'][0][0][2,:]
	qy = particles['ParticlePhaseAttributes'][0][0][3,:]
	qx[np.where(qx>0.5)] -= 1
	qy[np.where((qy>0.7) & (qx<0.2))] -= 1

	resonances = resonance_lines((3.55, 4.6),(3.55, 4.6),(1,2,3),16)
	fontsize=17
	f, ax = plt.subplots(1,figsize=(6,6))
	my_cmap = plt.cm.jet
	my_cmap.set_under('w',1)
	ax.hist2d(4+qx, 4+qy,bins=1000, cmap=my_cmap, vmin=1) #, norm=mcolors.PowerNorm(gamma))
	resonances.plot_resonance(f)
	ax.xaxis.label.set_size(fontsize)
	ax.yaxis.label.set_size(fontsize)
	ax.tick_params(labelsize=fontsize)
	plt.title('turn %s'%turn, fontsize=fontsize)
	plt.tight_layout()
	f.savefig('png/tune_diagram_%s.png'%turn, dpi=500)


plt.show()
print 'DONE'
