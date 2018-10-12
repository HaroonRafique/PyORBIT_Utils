import numpy as np

q1, q2, betax2L1_V_ROT, betay2L1_V_ROT, dispx2L1_V_ROT, dispy2L1_V_ROT, betax2L1_H_ROT, betay2L1_H_ROT, dispx2L1_H_ROT, dispy2L1_H_ROT = np.loadtxt('model', unpack=True, comments='*',skiprows=8)

qx=np.array(4*q1.tolist())
qy=np.array(4*q2.tolist())

betax=betax2L1_V_ROT
betax=np.append(betax,betax2L1_H_ROT)

betay=betay2L1_V_ROT
betay=np.append(betay,betay2L1_H_ROT)

dispx=dispx2L1_V_ROT
dispx=np.append(dispx,dispx2L1_H_ROT)

#dispx=9.144428e-01*dispx

dispy=dispy2L1_V_ROT
dispy=np.append(dispy,dispy2L1_H_ROT)

wire=np.zeros(4*len(betax2L1_V_ROT))

wire[:len(betax2L1_V_ROT)]='1'
wire[len(betax2L1_V_ROT):]='2'

l=[]

for i in range(len(betax)):
    l.append((qx[i],qy[i], wire[i],betax[i],betay[i],dispx[i],dispy[i]))
    print qx[i], ',', qy[i]

np.savetxt('optic_values_new.dat', l)


