import os
import numpy as np
import scipy.io as sio
import pylab as plt
import glob
import imageio

class resonance_lines(object):
	
	def __init__(self, Qx_range, Qy_range, orders, periodicity):
		
		if np.std(Qx_range):
			self.Qx_min = np.min(Qx_range)
			self.Qx_max = np.max(Qx_range)
		else:
			self.Qx_min = np.floor(Qx_range)-0.05
			self.Qx_max = np.floor(Qx_range)+1.05
		if np.std(Qy_range):
			self.Qy_min = np.min(Qy_range)
			self.Qy_max = np.max(Qy_range)
		else:
			self.Qy_min = np.floor(Qy_range)-0.05
			self.Qy_max = np.floor(Qy_range)+1.05

		self.periodicity = periodicity
									
		nx, ny = [], []

		for order in np.nditer(np.array(orders)):
			t = np.array(range(-order, order+1))
			nx.extend(order - np.abs(t))
			ny.extend(t)
		nx = np.array(nx)
		ny = np.array(ny)
	
		cextr = np.array([nx*np.floor(self.Qx_min)+ny*np.floor(self.Qy_min), \
						  nx*np.ceil(self.Qx_max)+ny*np.floor(self.Qy_min), \
						  nx*np.floor(self.Qx_min)+ny*np.ceil(self.Qy_max), \
						  nx*np.ceil(self.Qx_max)+ny*np.ceil(self.Qy_max)], dtype='int')
		cmin = np.min(cextr, axis=0)
		cmax = np.max(cextr, axis=0)
		res_sum = [range(cmin[i], cmax[i]+1) for i in xrange(cextr.shape[1])]								
		self.resonance_list = zip(nx, ny, res_sum)
		
	def plot_resonance(self, figure_object = None):	
		plt.ion()
		if figure_object:
			fig = figure_object
			plt.figure(fig.number)
		else:
			fig = plt.figure()
		Qx_min = self.Qx_min
		Qx_max = self.Qx_max
		Qy_min = self.Qy_min
		Qy_max = self.Qy_max 
		plt.xlim(Qx_min, Qx_max)
		plt.ylim(Qy_min, Qy_max)
		plt.xlabel('Qx')
		plt.ylabel('Qy')		
		for resonance in self.resonance_list:
			nx = resonance[0]
			ny = resonance[1]
			for res_sum in resonance[2]:		
				if ny:
					line, = plt.plot([Qx_min, Qx_max], \
					    [(res_sum-nx*Qx_min)/ny, (res_sum-nx*Qx_max)/ny])
				else:
					line, = plt.plot([np.float(res_sum)/nx, np.float(res_sum)/nx],[Qy_min, Qy_max])
				if ny%2:
					plt.setp(line, linestyle='--') # for skew resonances
				if res_sum%self.periodicity:
					plt.setp(line, color='b')	# non-systematic resonances
				else:
					plt.setp(line, color='r', linewidth=2.0) # systematic resonances
		plt.draw()
		return fig
		
	def print_resonances(self):
		for resonance in self.resonance_list:
			for res_sum in resonance[2]:
				'''
				print str(resonance[0]).rjust(3), 'Qx ', ("+", "-")[resonance[1]<0], \
					  str(abs(resonance[1])).rjust(2), 'Qy = ', str(res_sum).rjust(3), \
					  '\t', ("(non-systematic)", "(systematic)")[res_sum%self.periodicity==0]
				'''
				print '%s %s%s = %s\t%s'%(str(resonance[0]).rjust(2), ("+", "-")[resonance[1]<0], \
						str(abs(resonance[1])).rjust(2), str(res_sum).rjust(4), \
						("(non-systematic)", "(systematic)")[res_sum%self.periodicity==0])


plt.close('all')

# source_dir = 'input/'
source_dir = './'

filename = 'mainbunch'
files = glob.glob(source_dir + filename + '*.mat')
files.sort()

for i, file in enumerate(files[::-1]):
	print file
	try: 
		turn = int(file.split('mainbunch_')[-1][:-4])
		turn = '%04d'%turn
	except:
		turn = ''
	particles = sio.loadmat(file, squeeze_me=True,  struct_as_record=False)['particles'];
	x  = particles.x;
	xp = particles.xp;
	y  = particles.y;
	yp = particles.yp;
	z  = particles.z;
	dE = particles.dE;

	fontsize=15;

	qx = particles.ParticlePhaseAttributes[2,:];
	qy = particles.ParticlePhaseAttributes[3,:];
	qx[np.where(qx>0.5)] -= 1;
	qy[np.where((qy>0.6) & (qx<0.25))] -= 1;

	resonances = resonance_lines((5.75, 6.25),(5.75, 6.25),(1,2,3,4),10);
	fontsize=17;
	
	f, ax = plt.subplots(1, figsize=(6,6))
	gridspec.GridSpec(3,3)
	#f.subplots_adjust(hspace = 0)	# Horizontal spacing between subplots
	f.subplots_adjust(wspace = 0)	# Vertical spacing between subplots

	my_cmap = plt.cm.jet;
	my_cmap.set_under('w',1);

	r = resonances;

	# First subplot
	plt.subplot2grid((3,3), (0,0), colspan=2, rowspan=1)   
	plt.hist(6+qx, bins=1000, range=(r.Qx_min, r.Qx_max)) #, norm=mcolors.PowerNorm(gamma))
	plt.ylabel('Frequency')
	plt.grid(which='both')

	plt.title(r'(Q$_x$, Q$_y$) = (6.21, 6.10) turn %s'%turn, fontsize=fontsize);

	# Main plot
	plt.subplot2grid((3,3), (1,0), colspan=2, rowspan=2)
	plt.hist2d(6+qx, 6+qy, bins=1000, cmap=my_cmap, vmin=1, range=[[r.Qx_min, r.Qx_max], [r.Qy_min, r.Qy_max]]) #, norm=mcolors.PowerNorm(gamma))
	plt.xlabel(r'Q$_x$')
	plt.ylabel(r'Q$_y$')
	resonances.plot_resonance(f)

	# Second subplot
	plt.subplot2grid((3,3), (1,2), colspan=1, rowspan=2)    
	plt.hist(6+qy, bins=1000, range=(r.Qy_min, r.Qy_max), orientation=u'horizontal') #, norm=mcolors.PowerNorm(gamma))
	plt.xlabel('Frequency')
	plt.grid(which='both')

	current_axis = plt.gca()
	#current_axis.axes.get_yaxis().set_visible(False)

	ax.xaxis.label.set_size(fontsize)
	ax.yaxis.label.set_size(fontsize)

	ax.tick_params(labelsize=fontsize)

	plt.tight_layout()
	f.savefig('tune_diagram_%s.png'%turn, dpi=100);
	gifnames.append(savename)
	f.savefig(savename, dpi=500)
	plt.close(f)

	ax.hist2d(6+qx, 6+qy, bins=1000, cmap=my_cmap, vmin=1, range=[[r.Qx_min, r.Qx_max], [r.Qy_min, r.Qy_max]]); #, norm=mcolors.PowerNorm(gamma))
	resonances.plot_resonance(f);
	ax.xaxis.label.set_size(fontsize);
	ax.yaxis.label.set_size(fontsize);
	ax.tick_params(labelsize=fontsize);
	plt.tight_layout();
	plt.close(f);

# ~ plt.show()
print 'Individual Plots Complete'

filenames_all = glob.glob(source_dir + 'tune_diagram' + '*.png')
filenames_all.sort()

images = []
for filename in filenames_all:
    images.append(imageio.imread(filename))
imageio.mimsave('621_610_png.gif', images, duration=(1./6.))
print 'GIF Complete'
