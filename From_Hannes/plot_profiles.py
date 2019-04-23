import matplotlib.pylab as plt
import scipy.io as sio
import numpy as np
import glob
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import matplotlib.cm as cm
import os
import glob
# import mystyle as ms
fsize=16
# ms.mystyle_arial(fontsz=fsize, dist_tick_lab=10)

def _Gauss(x,x0,a,sigma):
	return a*exp(-(x-x0)**2/(2*sigma**2))

def GaussianFit(x, y):
	mean = sum(x*y)/sum(y)
	sigma = np.sqrt(sum(y*(x-mean)**2)/sum(y))
	amplitude = max(y)
	popt,pcov = curve_fit(_Gauss,x,y,p0=[mean,amplitude,sigma])
	amplitude_norm = popt[1]*np.sqrt(2*np.pi)/(x[1]-x[0]) * popt[2] / np.float(sum(y))
	# print amplitude_norm
	return popt, amplitude_norm

def _DoubleGauss(x,mu,ampl1,sigma1,ampl2,sigma2):
	# return abs(ampl1)*np.exp(-(x-mu)**2/(2*sigma1**2)) + abs(ampl2)*np.exp(-(x-mu)**2/(2*sigma2**2))
	return abs(ampl1)*np.exp(-(x-mu)**2/(2*sigma1**2)) + abs(ampl2)*np.exp(-(x-mu)**2/(2*sigma2**2))

def DoubleGaussianFit(x,y):
	try:
		p,_ = GaussianFit(x,y)
		popt,pcov = curve_fit(_DoubleGauss,x,y,p0=[p[0],p[1]*0.95,p[2],p[1]*0.05,2*p[2]]) #, bounds=([-1.,-1e9, 0., -1e9, 0.], [1., 1e9, 1., 1e9, 1.]))
		d = x[1]-x[0]
		s = np.float(sum(y))
		if abs(popt[1])>abs(popt[3]):
			A1 = abs(popt[1])
			sig1 = abs(popt[2])
			A2 = abs(popt[3])
			sig2 = abs(popt[4])
		else:
			A1 = abs(popt[3])
			sig1 = abs(popt[4])			
			A2 = abs(popt[1])
			sig2 = abs(popt[2])
		A1_norm = A1*np.sqrt(2*np.pi)/d * sig1 / s
		A2_norm = A2*np.sqrt(2*np.pi)/d * sig2 / s
		# print A1_norm, A2_norm, A1_norm + A2_norm
		return {'mu': popt[0], 'A1': A1, 'sig1': sig1, 'A2': A2, 'sig2': sig2, 'A1_norm': A1_norm, 'A2_norm': A2_norm, 'pcov': pcov, 'p': popt}
	except:
		return {k: np.nan for k in ['mu', 'A1', 'sig1', 'A2', 'sig2', 'pcov', 'p', 'A1_norm', 'A2_norm']}

def calculate_second_moment(x, y, y_thresh_rel=0.02):
    # y -= min(y)
    # y -= np.median(y)
    y = y/max(y)
    i_filtered = np.where(y>y_thresh_rel)
    x_f = x[i_filtered]
    y_f = y[i_filtered]
    W = sum(y_f)
    mu = np.sum(x_f*y_f)/W
    sig = np.sqrt(np.sum(y_f*(x_f-mu)**2)/W)
    return sig, mu, x_f, y_f



png_dir = 'png'
for d in [png_dir]:
	if not os.path.exists(d):
		os.mkdir(d)


plt.close('all')

# beta = {'x': 104, 'y':32.3, 'z':1}
# betagamma = 27.7


# t_rev = 2*np.pi*1100/3e8

# start lattice at 519 (we scale vertical profile to location of 416)
# sqrt_betx_ratio = 1.0 	#np.sqrt(86.8/104.26)  
# sqrt_bety_ratio = np.sqrt(71./38.82454639)	#np.sqrt(71./32.3)

# second_moment_ratio = {'x': [], 'y': [], 'z': []}
# intensity_ratio = []
# freq_summary = []



positions, amplitudes = {'x':[], 'y': [], 'z': []}, {'x':[], 'y': [], 'z': []}
turns = []

files = sorted(glob.glob('Output/bunch_profile_*.mat'))
files_to_plot = files[::]
f, axs = plt.subplots(1,3,figsize=(12,4))
colors = cm.rainbow(np.linspace(0, 1, len(files_to_plot)))
for filename, c in zip(files_to_plot, colors):
	print filename
	with open(filename, 'r') as fid:
		a = sio.loadmat(fid, squeeze_me=True, struct_as_record=False)
		# turns.append(int(f.split('_')[-1].split('.mat')[0]))
		
		for i, u in enumerate(['x', 'y', 'z'][:]):
			pos = a[u][0]
			ampl = np.copy(a[u][1])
			axs[i].plot(pos, ampl, c=c)
			# second_moment[u].append(calculate_second_moment(pos,ampl,y_thresh_rel=0.0)[0])
			# profiles_pos[u].append(pos)
			# profiles_ampl[u].append(ampl/(pos[1]-pos[0]))
		# intensity.append(sum(a[u][1]))
axs[0].set_xlabel('x (m)')
axs[1].set_xlabel('y (m)')
axs[2].set_xlabel('z (m)')
axs[0].set_ylabel('counts')
axs[1].set_ylabel('counts')
axs[2].set_ylabel('counts')
plt.tight_layout()
plt.savefig('png/profiles.png', dpi=400)
plt.show()