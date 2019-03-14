import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import MyStyle as ms
ms.set_mystyle()

filename = 'Phi_grid.mat'

mat = sio.loadmat(filename)

Ex_grid = mat['Ex_grid']
Ey_grid = mat['Ey_grid']
phi_grid = mat['phi_grid']
x_grid = mat['x_grid']
y_grid = mat['y_grid']

print 'xmax =', np.max(x_grid), 'xmin =', np.min(x_grid)
print 'ymax =', np.max(y_grid), 'ymin =', np.min(y_grid)

# plotting ============
fig = plt.figure(0)
fig.clf()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(x_grid, y_grid, phi_grid, rstride=1, cstride=1, cmap=cm.jet,
        linewidth=0.2, antialiased=True, alpha=.7)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_zlabel('phi [a.u.]')
ax.view_init(elev=30., azim=-55)
plt.show()
plt.savefig("result.png", dpi=400)


fig = plt.figure(1)
fig.clf()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(x_grid, y_grid, Ey_grid, rstride=1, cstride=1, cmap=cm.jet,
        linewidth=0.2, antialiased=True, alpha=.7)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_zlabel('Ey [a.u.]')
ax.view_init(elev=30., azim=-55)
plt.show()
# plt.savefig("result.png", dpi=400)

