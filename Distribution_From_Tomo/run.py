import numpy as np
import matplotlib.pyplot as plt
import subprocess
import re

result = subprocess.Popen(['tomo_vo.intelmp'],
stdin=open("measure.dat", 'r'), stdout=subprocess.PIPE,
stderr=subprocess.PIPE)

out, err = result.communicate()

out = out.splitlines()
print(out)

dat = np.loadtxt("image001.data")
dat = dat.reshape([np.sqrt(dat.shape[0])]*2).T

regexp = re.compile("\\d+\\.?\\d*E?[-+]?\\d*")

print(out[7])
print(out[9])

dt = float(regexp.findall(out[7])[0])
dE = float(regexp.findall(out[9])[0])

tAxis = np.arange(dat.shape[0])*dt
EAxis = np.arange(dat.shape[0])*dE

tAxis -= np.mean(tAxis)
EAxis -= np.mean(EAxis)

plt.pcolor(tAxis, EAxis, dat)
plt.show()
