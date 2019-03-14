import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import MyStyle as ms
ms.set_mystyle()

filename = 'Phi_grid.mat'
mat = sio.loadmat(filename)

value_grid = mat['Ex_grid']; zlabel = 'Ex [a.u.]' 
# value_grid = mat['Ey_grid']; zlabel = 'Ey [a.u.]' 
# value_grid = mat['phi_grid']; zlabel = 'phi [a.u.]' 
x_grid = mat['x_grid']
y_grid = mat['y_grid']

print 'xmin =', np.min(x_grid), 'xmax =', np.max(x_grid)
print 'ymin =', np.min(y_grid), 'ymax =', np.max(y_grid)

filename2 = 'kicks.mat'
mat2 = sio.loadmat(filename2)
x = mat2['x']
xp = mat2['xp']
y = mat2['y']
yp = mat2['yp']
slope_theory_x = mat2['slope_theory_x']
slope_theory_y = mat2['slope_theory_y']

# plotting ===========
fig = plt.figure(5)
fig.clf()
ax = fig.gca()
line_PIC, = plt.plot(x.T, xp.T, '.', label='PIC calculation')
line_Theory, = plt.plot(x.T, x.T*slope_theory_x, 'r', label='Theory')
ax.set_xlabel('x [m]')
ax.set_ylabel('xp kick')
plt.legend(loc=2)
fig.set_size_inches(5.5, 5)
plt.show()
plt.savefig("result1.pdf")

fig = plt.figure(4)
fig.clf()
ax = fig.gca(projection='3d')
# value_grid[value_grid<0] = 0
surf = ax.plot_surface(x_grid, y_grid, value_grid, rstride=1, cstride=1, cmap=cm.jet,
        linewidth=0.2, antialiased=True, alpha=.7)
ax.view_init(elev=20., azim=119)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_zlabel(zlabel)
plt.show()
plt.savefig("result2.pdf")

	
