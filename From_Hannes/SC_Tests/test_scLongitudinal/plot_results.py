import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import MyStyle as ms
ms.set_mystyle()


filename = 'output.mat'
mat = sio.loadmat(filename)
# print  mat.keys()

x = mat['x'].flatten()
y = mat['y'].flatten()
z = mat['z'].flatten()
sc_kick_1D = mat['sc_kick_1D'].flatten()
sc_kick_2p5Drb = mat['sc_kick_2p5Drb'].flatten()
sc_kick_SliceBySlice = mat['sc_kick_SliceBySlice'].flatten()

z_test = mat['z_test'].flatten()
sc_kick_theory = mat['sc_kick_theory'].flatten()


# plotting ===========
plot_every = 200
fig = plt.figure(1)
fig.clf()
ax = fig.gca()
line_1D = ax.plot(z[::plot_every], sc_kick_1D[::plot_every], 'b.', label='SC impedance')
# line_2p5Drb = ax.plot(z[::plot_every], sc_kick_2p5Drb[::plot_every], 'm.', label='2.5D RB')
line_SbS2D = ax.plot(z[::plot_every], sc_kick_SliceBySlice[::plot_every], 'g.', label='Slice-By-Slice 2D')
line_Analytical = ax.plot(z_test, sc_kick_theory, 'r', label='Theroy (beam center)')
plt.legend(loc=2)
ax.set_xlabel('z [m]')
ax.set_ylabel('dE kick [GeV]')
plt.show()
plt.savefig("result_c.pdf")

'''


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
'''
