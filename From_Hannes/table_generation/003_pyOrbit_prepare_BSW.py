import numpy as np
import matplotlib.pylab as plt
import datetime
from lib import metaclass
from lib.write_ptc_table import write_PTCtable
from lib.mpi_helpers import mpi_mkdir_p

mpi_mkdir_p('Tables')

b = metaclass.twiss('PSB/output/BSW_betabeat_correction.tfs')

t = b.BSW_T
multipole_orders = [1,3]
write_PTCtable('Tables/BI1.BSW1L1.1.dat', multipole_orders, t, [b.BSW1_K0, b.BSW1_K2], [b.BSW1_K0*0, b.BSW1_K2*0])
write_PTCtable('Tables/BI1.BSW1L1.2.dat', multipole_orders, t, [b.BSW2_K0, b.BSW2_K2], [b.BSW2_K0*0, b.BSW2_K2*0])
write_PTCtable('Tables/BI1.BSW1L1.3.dat', multipole_orders, t, [b.BSW3_K0, b.BSW3_K2], [b.BSW3_K0*0, b.BSW3_K2*0])
write_PTCtable('Tables/BI1.BSW1L1.4.dat', multipole_orders, t, [b.BSW4_K0, b.BSW4_K2], [b.BSW4_K0*0, b.BSW4_K2*0])

multipole_orders = 2
write_PTCtable('Tables/QDE3_CompAll.dat',    multipole_orders, t, b.KD3, b.KD3*0)
write_PTCtable('Tables/QDE14_CompAll.dat',   multipole_orders, t, b.KD14, b.KD14*0)
write_PTCtable('Tables/QDEstd_CompAll.dat',  multipole_orders, t, b.KKD, b.KKD*0)
write_PTCtable('Tables/QFOstd_CompAll.dat',  multipole_orders, t, b.KKF, b.KKF*0)




