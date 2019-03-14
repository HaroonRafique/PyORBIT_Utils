import scipy.io as sio
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


Efield = sio.loadmat('out.mat')

value_grid = Efield['Ey']

fig = plt.figure(0)
fig.clf()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(Efield['xv'], Efield['yv'], value_grid.T, rstride=1, cstride=1, cmap=cm.jet,
        linewidth=0.2, antialiased=True, alpha=.7)
plt.show()
