import numpy as np

q1, q2, betax64, betay64, dispx64, dispy64, betax65, betay65, dispx65, dispy65, betax68, betay68, dispx68, dispy68, betax85, betay85, dispx85, dispy85= np.loadtxt('model', unpack=True, comments='*',skiprows=8)

qx=np.array(4*q1.tolist())
qy=np.array(4*q2.tolist())

betax=betax64
betax=np.append(betax,betax65)
betax=np.append(betax,betax68)
betax=np.append(betax,betax85)

betay=betay64
betay=np.append(betay,betay65)
betay=np.append(betay,betay68)
betay=np.append(betay,betay85)

dispx=dispx64
dispx=np.append(dispx,dispx65)
dispx=np.append(dispx,dispx68)
dispx=np.append(dispx,dispx85)

dispx=9.144428e-01*dispx

dispy=dispy64
dispy=np.append(dispy,dispy65)
dispy=np.append(dispy,dispy68)
dispy=np.append(dispy,dispy85)

wire=np.zeros(4*len(betax64))

wire[:len(betax64)]=64
wire[len(betax64):2*len(betax64)]=65
wire[2*len(betax64):3*len(betax64)]=68
wire[3*len(betax64):]=85

l=[]

for i in range(len(betax)):
    l.append((qx[i],qy[i], wire[i],betax[i],betay[i],dispx[i],dispy[i]))
    print qx[i], ',', qy[i]

np.savetxt('optic_values_new.dat', l)


