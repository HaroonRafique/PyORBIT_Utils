import collections
import os
import re
import shutil
import sys
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
from scipy.io import savemat
sys.path.append('../')
#from util import get_column


E_rest = 0.938272e9  # Rest mass in [eV/c^2] of accelerated particle
q = 1  # Charge of accelerated particle
#ctime = [297, 357, 427, 486, 536, 586, 636, 686, 736, 796]
ctime = [297]
rho = 8.239  # Bending radius in [m]
C = 299792458  # Speed of ligh in [m/s]

# Functions
def get_dpp(sigmaE, gamma0, E_rest):
    return sigmaE / ((gamma0 - 1 / gamma0) * E_rest)


def get_gamma0(q, b, rho, C, E_rest):
    return np.sqrt(1 + ((q * b * rho * C / E_rest) * (q * b * rho * C / E_rest)))


def get_sigmaE(dEbin, yms, ybar):
    return dEbin * np.sqrt(yms - ybar**2)


def get_fortran_output(f_output, string):
    try:
        with open(f_output, 'r') as f:
            for line in f:
                if re.search(string, line) is not None:
                    return float(line.replace(string, '').replace(' = ', ''))
    except FileNotFoundError:
        sys.exit('>> Remove/rename tomogram file for this ctime and run the script again.')


def get_yms_ybar(infile, profilelength):
    data = np.ndarray(shape=(profilelength, profilelength), buffer=np.array(np.loadtxt(infile)))
    xbar = []
    ybar = []
    xms = []
    yms = []
    for i in range(0, profilelength):
        for j in range(0, profilelength):
            xbar.append(data[i, j] * (i + 1))
            ybar.append(data[i, j] * (j + 1))
            xms.append(data[i, j] * (i + 1) ** 2)
            yms.append(data[i, j] * (j + 1) ** 2)
    return float(sum(yms)), float(sum(ybar))


def get_bfield(ctime):
    b = []
    data = np.loadtxt(os.path.join(tomo_folder, 'bfield.txt'))
    for line in data:
        if str(int(line[0])) == ctime or str(int(line[0])) == str(int(ctime) + 1) or  str(int(line[0])) == str(int(ctime) - 1) or str(int(line[0])) == str(int(ctime) + 2) or str(int(line[0])) == str(int(ctime) - 2):
            b = float(line[1])
        else:
            continue
    return b


def plot_tomogram(infile, profilelength, ctime, dE, dt, x, y, dpp, eperimage, gamma0):
    data = np.ndarray(shape=(profilelength, profilelength), buffer=np.array(np.loadtxt(infile)))
    # PLOT --------------------------------------------------------
    fig = plt.figure()
    gs = GridSpec(3, 3)  # 2 rows, 2 columns
    ax1 = fig.add_subplot(gs[0, 0:2])  # First row, first column
    ax2 = fig.add_subplot(gs[1:3, 2])  # First row, second column
    ax3 = fig.add_subplot(gs[1:3, 0:2])  # First row, third column
    ax4 = fig.add_subplot(gs[0, 2])  # First row, third column
    # -------------------------------------------------------------
    ax4.xaxis.set_major_formatter(plt.NullFormatter())
    ax4.yaxis.set_major_formatter(plt.NullFormatter())
    ax4.annotate('ctime: ' + str(ctime), xy=(0.05, 0.7), xytext=(0.05, 0.7))
    ax4.annotate('dp/p: ' + '{:.4E}'.format(dpp), xy=(0.05, 0.5), xytext=(0.05, 0.5))
    ax4.axis('off')
    # -------------------------------------------------------------
    ax3.pcolor(np.transpose(data))
    ax3.set_xlim([0, profilelength])
    ax3.set_ylim([0, profilelength])
    ax3.set_xlabel('Time [ns]')
    ax3.set_ylabel('Energy [MeV]')
    # -------------------------------------------------------------
    labels_x = [item.get_text() for item in ax3.get_xticklabels()]
    labels_x = ax3.get_xticks().tolist()
    for i, l in enumerate(labels_x):
        labels_x[i] = int(round((l - x) * dt * 1e9, 0))
    ax3.set_xticklabels(labels_x)
    # -------------------------------------------------------------
    labels_y = [item.get_text() for item in ax3.get_yticklabels()]
    labels_y = ax3.get_yticks().tolist()
    for i, l in enumerate(labels_y):
        labels_y[i] = round((l - y) * dE * 1e-6, 1)
    ax3.set_yticklabels(labels_y)
    # -------------------------------------------------------------
    ax1.plot(np.sum(data, axis=1) * 0.36 * profilelength) # Effective pick-up sensitivity (in digitizer units per instantaneous Amp)
    ax1.set_xlim([0, profilelength])
    ax1.set_ylabel('Current [A]')
    ax1.xaxis.set_major_formatter(plt.NullFormatter())
    # -------------------------------------------------------------
    x_ax2 = np.linspace(0, len(np.sum(data, axis=0)), len(np.sum(data, axis=0)))
    ax2.plot(np.sum(data, axis=0), x_ax2)
    ax2.set_ylim([0, profilelength])
    ax2.yaxis.set_major_formatter(plt.NullFormatter())
    ax2.xaxis.set_major_formatter(plt.NullFormatter())
    plt.show()

ctime = '297'
tomo_folder = './tomoscope'

b = get_bfield(ctime)
print('>> B field =', '{:.4E}'.format(b))
dEbin = get_fortran_output(tomo_folder + '/output_' + str(ctime) + '.txt', 'dEbin')
dt = get_fortran_output(tomo_folder + '/output_' + str(ctime) + '.txt', 'dtbin')
x = get_fortran_output(tomo_folder + '/output_' + str(ctime) + '.txt', 'xat0')
y = get_fortran_output(tomo_folder + '/output_' + str(ctime) + '.txt', 'yat0')
eperimage = get_fortran_output(tomo_folder + '/output_' + str(ctime) + '.txt', 'eperimage')
profilelength = int(get_fortran_output(tomo_folder + '/output_' + str(ctime) + '.txt', 'profilelength'))
yms, ybar = get_yms_ybar(os.path.join(tomo_folder, 'image_' + str(ctime) + '.data'), profilelength)
sigmaE = get_sigmaE(dEbin, yms, ybar)
gamma0 = get_gamma0(q, b, rho, C, E_rest)
dpp = get_dpp(sigmaE, gamma0, E_rest)
print('>> dp/p value =', '{:.4E}'.format(dpp))
print('')

infile = os.path.join(tomo_folder, 'image_' + str(ctime) + '.data')
data = np.ndarray(shape=(profilelength, profilelength), buffer=np.array(np.loadtxt(infile)))
data = np.transpose(data)

# Make time and energy vector
time_in_bins = np.arange(0, profilelength)
time_in_nsec = (time_in_bins - x) * dt * 1e9

energy_in_bins = np.arange(0, profilelength)
energy_in_MeV = (energy_in_bins - y) * dEbin * 1e-6

yy, xx = np.meshgrid(energy_in_MeV, time_in_nsec)
plt.pcolormesh(xx, yy, data.T)
plt.xlabel('Time (ns)')
plt.ylabel('Energy (MeV)')
plt.show()

data_dict = {'time_nsec': time_in_nsec, 'energy_MeV': energy_in_MeV, 'density_array': data}
savemat('tomo_data_singleRF_EKP_{:d}.mat'.format(int(ctime)), data_dict)

'''
#plot_tomogram(os.path.join(tomo_folder, 'image_' + str(ctime) + '.data'), profilelength, ctime, dEbin, dt, x, y, dpp, eperimage, gamma0)

from scipy.io import loadmat

plt.figure(1000)
dct = loadmat('tomo_data_singleRF_EKP_{:d}.mat'.format(int(ctime)))
yy, xx = np.meshgrid(dct['energy_MeV'], dct['time_nsec'])
plt.pcolormesh(xx, yy, dct['density_array'].T)
plt.xlabel('Time (ns)')
plt.ylabel('Energy (MeV)')
plt.show()
'''
