import numpy as np
import pylab as plt
import matplotlib 
matplotlib.style.use('classic')

fig=plt.figure()
ax=plt.subplot(111, projection='polar')
skiprow = 26

# Test 3 & 11 L1

# ~ data=np.loadtxt('PTC-normal_1+2_XNO3L1.ptc', usecols=(3,5) ,unpack=True, skiprows=skiprow)
# ~ a=zip(['cos','sin','amplitude'],data[0,:3],data[1,:3])
# ~ print a
# ~ tans=a[0][2]/a[1][2]
# ~ phase=np.arctan2(a[0][2],a[1][2])

# ~ ax.plot([phase,phase], [0,a[2][2]],label='XNO3L1')

# ~ data=np.loadtxt('PTC-normal_1+2_XNO11L1.ptc', usecols=(3,5) ,unpack=True, skiprows=skiprow)
# ~ a=zip(['cos','sin','amplitude'],data[0,:3],data[1,:3])
# ~ print a
# ~ tans=a[0][2]/a[1][2]
# ~ phase=np.arctan2(a[0][2],a[1][2])

# ~ ax.plot([phase,phase], [0,a[2][2]],label='XNO11L1')

# Plot all (3+11) and (8+16) as grouped in WorkingSets

data=np.loadtxt('PTC-normal_1+2_XNO311L1.ptc', usecols=(3,5) ,unpack=True, skiprows=skiprow)
a=zip(['cos','sin','amplitude'],data[0,:3],data[1,:3])
print a
tans=a[0][2]/a[1][2]
phase=np.arctan2(a[0][2],a[1][2])

ax.plot([phase,phase], [0,a[2][2]],label='XNO311L1')

data=np.loadtxt('PTC-normal_1+2_XNO816L1.ptc', usecols=(3,5) ,unpack=True, skiprows=skiprow)
a=zip(['cos','sin','amplitude'],data[0,:3],data[1,:3])
tans=a[0][2]/a[1][2]
phase=np.arctan2(a[0][2],a[1][2])

ax.plot([phase,phase], [0,a[2][2]],label='XNO816L1')

data=np.loadtxt('PTC-normal_1+2_XNO4L1.ptc', usecols=(3,5) ,unpack=True, skiprows=skiprow)
a=zip(['cos','sin','amplitude'],data[0,:3],data[1,:3])
tans=a[0][2]/a[1][2]
phase=np.arctan2(a[0][2],a[1][2])

ax.plot([phase,phase], [0,a[2][2]],label='XNO4L1')

data=np.loadtxt('PTC-normal_1+2_XNO6L1.ptc', usecols=(3,5) ,unpack=True, skiprows=skiprow)
a=zip(['cos','sin','amplitude'],data[0,:3],data[1,:3])
tans=a[0][2]/a[1][2]
phase=np.arctan2(a[0][2],a[1][2])

ax.plot([phase,phase], [0,a[2][2]],label='XNO6L1')

data=np.loadtxt('PTC-normal_1+2_XNO9L1.ptc', usecols=(3,5) ,unpack=True, skiprows=skiprow)
a=zip(['cos','sin','amplitude'],data[0,:3],data[1,:3])
tans=a[0][2]/a[1][2]
phase=np.arctan2(a[0][2],a[1][2])

ax.plot([phase,phase], [0,a[2][2]],label='XNO9L1')

data=np.loadtxt('PTC-normal_1+2_XNO12L1.ptc', usecols=(3,5) ,unpack=True, skiprows=skiprow)
a=zip(['cos','sin','amplitude'],data[0,:3],data[1,:3])
tans=a[0][2]/a[1][2]
phase=np.arctan2(a[0][2],a[1][2])

ax.plot([phase,phase], [0,a[2][2]],label='XNO12L1')

ax.set_yticklabels([])
ax.tick_params(axis='both',which='major',labelsize=18)
plt.legend(loc=0,fontsize=16)
plt.savefig('Qv_1+2_rdts.png',dpi=300)
