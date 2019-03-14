import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import MyStyle as ms
ms.set_mystyle()


filename = 'output.mat'
mat = sio.loadmat(filename)
# print mat.keys()
x = mat['x'].flatten()
y = mat['y'].flatten()
z = mat['z'].flatten()
xp_Analytical = mat['xp_Analytical'].flatten()
yp_Analytical = mat['yp_Analytical'].flatten()
xp_2p5D = mat['xp_2p5D'].flatten()
yp_2p5D = mat['yp_2p5D'].flatten()
xp_SliceBySlice2D = mat['xp_SliceBySlice2D'].flatten()
yp_SliceBySlice2D = mat['yp_SliceBySlice2D'].flatten()
xp_3D = mat['xp_3D'].flatten()
yp_3D = mat['yp_3D'].flatten()
N_mp_test_x = mat['N_mp_test_x'].flatten()
N_mp_test_y = mat['N_mp_test_y'].flatten()
N_mp_test_z = mat['N_mp_test_z'].flatten()

# plotting ===========
fig = plt.figure(1)
fig.clf()
ax = fig.gca()
strt_indx = len(x)-N_mp_test_x-N_mp_test_y-N_mp_test_z # test particles are at the end: x, then y, then z
stop_indx = len(x)-N_mp_test_y-N_mp_test_z
line_2p5D = ax.plot(x[strt_indx:stop_indx], xp_2p5D[strt_indx:stop_indx], 'b.', label='PIC 2.5D')
line_SbS2D = ax.plot(x[strt_indx:stop_indx], xp_SliceBySlice2D[strt_indx:stop_indx], 'g.', label='PIC slice-by-slice 2D')
# line_SbS2D = ax.plot(x[strt_indx:stop_indx], xp_3D[strt_indx:stop_indx], 'g.', label='PIC 3D')
line_Analytical = ax.plot(x[strt_indx:stop_indx], xp_Analytical[strt_indx:stop_indx], 'r', label='Bassetti Erskine')
plt.legend(loc=2)
ax.set_xlabel('x [m]')
ax.set_ylabel('xp kick')
plt.show()
plt.savefig("result_x.pdf")


fig = plt.figure(2)
fig.clf()
ax = fig.gca()
strt_indx = len(x)-N_mp_test_y-N_mp_test_z # test particles are at the end: x, then y, then z
stop_indx = len(x)-N_mp_test_z
line_2p5D = ax.plot(y[strt_indx:stop_indx], yp_2p5D[strt_indx:stop_indx], 'b.', label='PIC 2.5D')
line_SbS2D = ax.plot(y[strt_indx:stop_indx], yp_SliceBySlice2D[strt_indx:stop_indx], 'g.', label='PIC slice-by-slice 2D')
# line_SbS2D = ax.plot(y[strt_indx:stop_indx], yp_3D[strt_indx:stop_indx], 'g.', label='PIC 3D')
line_Analytical = ax.plot(y[strt_indx:stop_indx], yp_Analytical[strt_indx:stop_indx], 'r', label='Bassetti Erskine')
plt.legend(loc=2)
ax.set_xlabel('y [m]')
ax.set_ylabel('yp kick')
plt.show()
plt.savefig("result_y.pdf")


fig = plt.figure(3)
fig.clf()
ax = fig.gca()
strt_indx = len(x)-N_mp_test_z # test particles are at the end: x, then y, then z
stop_indx = len(x) 
line_2p5D = ax.plot(z[strt_indx:stop_indx], xp_2p5D[strt_indx:stop_indx], 'b.', label='PIC 2.5D')
line_SbS2D = ax.plot(z[strt_indx:stop_indx], xp_SliceBySlice2D[strt_indx:stop_indx], 'g.', label='PIC slice-by-slice 2D')
# line_SbS2D = ax.plot(z[strt_indx:stop_indx], xp_3D[strt_indx:stop_indx], 'g.', label='PIC 3D')
line_Analytical = ax.plot(z[strt_indx:stop_indx], xp_Analytical[strt_indx:stop_indx], 'r.', label='Bassetti Erskine')
plt.legend(loc=8)
ax.set_xlabel('z [m]')
ax.set_ylabel('xp kick')
plt.show()
plt.savefig("result_z.pdf")

fig = plt.figure(4)
fig.clf()
ax = fig.gca()
strt_indx = 0 
stop_indx = 10000
line_2p5D = ax.plot(xp_Analytical[strt_indx:stop_indx], xp_2p5D[strt_indx:stop_indx], 'b.', label='PIC 2.5D')
line_SbS2D = ax.plot(xp_Analytical[strt_indx:stop_indx], xp_SliceBySlice2D[strt_indx:stop_indx], 'g.', label='PIC slice-by-slice 2D')
# line_SbS2D = ax.plot(xp_Analytical[strt_indx:stop_indx], xp_3D[strt_indx:stop_indx], 'g.', label='PIC 3D')
# line_Analytical = ax.plot(xp_Analytical[strt_indx:stop_indx], xp_Analytical[strt_indx:stop_indx], 'r', label='Bassetti Erskine')
plt.legend(loc=2)
ax.set_xlabel('xp kick (Bassetti Erskine)')
ax.set_ylabel('xp kick')
plt.show()
# plt.savefig("result.pdf")

