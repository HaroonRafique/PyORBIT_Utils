import numpy as np
import matplotlib.pyplot as plt
import subprocess
import re

input_file='2017.11.28.12.09.05.117_tomo185.dat'
full_input_file='./2017.11.28.12.09.05.117_tomo185.dat'

# ~ result = subprocess.Popen(['./tomo_vo.intelmp'], stdin=open("./2017.11.28.12.08.05.116_tomo185.dat", 'r'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
result = subprocess.Popen(['./tomo_vo.intelmp'], stdin=open(full_input_file, 'r'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = result.communicate()

out = out.splitlines()
# ~ print(out)

dat = np.loadtxt("image002.data")
print dat
var = (int(np.sqrt(dat.shape[0])), int(np.sqrt(dat.shape[0])))
dat = dat.reshape(var).T

print dat.shape

regexp = re.compile("\\d+\\.?\\d*E?[-+]?\\d*")

print(out[7])
print(out[9])

dt = float(regexp.findall(out[7])[0])/1E-9
dE = float(regexp.findall(out[9])[0])/1E9

tAxis = np.arange(dat.shape[0])*dt
EAxis = np.arange(dat.shape[0])*dE

tAxis -= np.mean(tAxis)
EAxis -= np.mean(EAxis)

fig, ax = plt.subplots()

ax.pcolor(tAxis, EAxis, dat)

ax.set(xlabel='dt [ns]', ylabel='dE [GeV]', title='Longitudinal distribution from tomo data')

# ~ plt.show()
plot_name = input_file + '.png'
fig.savefig(plot_name, dpi=600)
