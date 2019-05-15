# Plot Courant-Snyder parameters calculated in PTC and PyORBIT to 
# compare

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['figure.figsize'] = [4.0, 3.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.rcParams['font.size'] = 6
plt.rcParams['legend.fontsize'] = 'medium'
plt.rcParams['figure.titlesize'] = 'medium'

plt.rcParams['lines.linewidth'] = 1

beta = 0.915961016423
gamma =	2.49210461976

xmax = 630

plot_610 = True
plot_614 = True
plot_624 = True

plot_LEQ = True
plot_PFW = False

# Open Files
leq_610_file = 'LEQ_610/ptc_twiss'
leq_610_s = []
leq_610_betx = []
leq_610_bety = []
leq_610_alfx = []
leq_610_alfy = []
leq_610_Dx = []

pfw_610_file = 'PFW_610/ptc_twiss'
pfw_610_s = []
pfw_610_betx = []
pfw_610_bety = []
pfw_610_alfx = []
pfw_610_alfy = []
pfw_610_Dx = []

leq_614_file = 'LEQ_614/ptc_twiss'
leq_614_s = []
leq_614_betx = []
leq_614_bety = []
leq_614_alfx = []
leq_614_alfy = []
leq_614_Dx = []

pfw_614_file = 'PFW_614/ptc_twiss'
pfw_614_s = []
pfw_614_betx = []
pfw_614_bety = []
pfw_614_alfx = []
pfw_614_alfy = []
pfw_614_Dx = []

leq_624_file = 'LEQ_624/ptc_twiss'
leq_624_s = []
leq_624_betx = []
leq_624_bety = []
leq_624_alfx = []
leq_624_alfy = []
leq_624_Dx = []

pfw_624_file = 'PFW_624/ptc_twiss'
pfw_624_s = []
pfw_624_betx = []
pfw_624_bety = []
pfw_624_alfx = []
pfw_624_alfy = []
pfw_624_Dx = []

print 'Reading 610 LEQ file'
fin1=open(leq_610_file,'r').readlines()[90:]

for f in fin1:
	#name, s, betx, bety, alfx, alfy, disp1, disp1p
    leq_610_s.append(float(f.split()[0]))
    leq_610_betx.append(float(f.split()[1]))
    leq_610_bety.append(float(f.split()[2]))
    leq_610_alfx.append(float(f.split()[3]))
    leq_610_alfy.append(float(f.split()[4]))
    leq_610_Dx.append(float(f.split()[5]))


print 'Reading 610 PFW file'
fin1=open(pfw_610_file,'r').readlines()[90:]

for f in fin1:
	#name, s, betx, bety, alfx, alfy, disp1, disp1p
    pfw_610_s.append(float(f.split()[0]))
    pfw_610_betx.append(float(f.split()[1]))
    pfw_610_bety.append(float(f.split()[2]))
    pfw_610_alfx.append(float(f.split()[3]))
    pfw_610_alfy.append(float(f.split()[4]))
    pfw_610_Dx.append(float(f.split()[5]))

print 'Reading 614 LEQ file'
fin1=open(leq_614_file,'r').readlines()[90:]

for f in fin1:
	#name, s, betx, bety, alfx, alfy, disp1, disp1p
    leq_614_s.append(float(f.split()[0]))
    leq_614_betx.append(float(f.split()[1]))
    leq_614_bety.append(float(f.split()[2]))
    leq_614_alfx.append(float(f.split()[3]))
    leq_614_alfy.append(float(f.split()[4]))
    leq_614_Dx.append(float(f.split()[5]))


print 'Reading 610 PFW file'
fin1=open(pfw_614_file,'r').readlines()[90:]

for f in fin1:
	#name, s, betx, bety, alfx, alfy, disp1, disp1p
    pfw_614_s.append(float(f.split()[0]))
    pfw_614_betx.append(float(f.split()[1]))
    pfw_614_bety.append(float(f.split()[2]))
    pfw_614_alfx.append(float(f.split()[3]))
    pfw_614_alfy.append(float(f.split()[4]))
    pfw_614_Dx.append(float(f.split()[5]))


print 'Reading 624 LEQ file'
fin1=open(leq_624_file,'r').readlines()[90:]

for f in fin1:
	#name, s, betx, bety, alfx, alfy, disp1, disp1p
    leq_624_s.append(float(f.split()[0]))
    leq_624_betx.append(float(f.split()[1]))
    leq_624_bety.append(float(f.split()[2]))
    leq_624_alfx.append(float(f.split()[3]))
    leq_624_alfy.append(float(f.split()[4]))
    leq_624_Dx.append(float(f.split()[5]))


print 'Reading 624 PFW file'
fin1=open(pfw_624_file,'r').readlines()[90:]

for f in fin1:
	#name, s, betx, bety, alfx, alfy, disp1, disp1p
    pfw_624_s.append(float(f.split()[0]))
    pfw_624_betx.append(float(f.split()[1]))
    pfw_624_bety.append(float(f.split()[2]))
    pfw_624_alfx.append(float(f.split()[3]))
    pfw_624_alfy.append(float(f.split()[4]))
    pfw_624_Dx.append(float(f.split()[5]))

#############
#   Beta x  #
#############
print 'Plotting beta_x'
fig, ax1 = plt.subplots();

plt.title(r"PTC $\beta_x$");

if plot_LEQ: ax1.plot(leq_610_s, leq_610_betx, color='b', label=r'Q$_y$ = 6.10 LEQ')
if plot_PFW: ax1.plot(pfw_610_s, pfw_610_betx, color='r', label=r'Q$_y$ = 6.10 PFW')
if plot_LEQ: ax1.plot(leq_624_s, leq_624_betx, color='k', label=r'Q$_y$ = 6.24 LEQ')
if plot_PFW: ax1.plot(pfw_624_s, pfw_624_betx, color='c', label=r'Q$_y$ = 6.24 PFW')
if plot_LEQ: ax1.plot(leq_614_s, leq_614_betx, color='m', label=r'Q$_y$ = 6.14 LEQ')
if plot_PFW: ax1.plot(pfw_614_s, pfw_614_betx, color='orange', label=r'Q$_y$ = 6.14 PFW')

ax1.set_xlabel("s [m]");
ax1.set_ylabel(r"$\beta_x$ [m]");

# Make the y-axis label, ticks and tick labels match the line color.
# ~ ax1.tick_params('y', colors='b');

ax1.set_xlim(0, xmax)

ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

ax1.legend(loc = 2);
ax1.set_ylim(10, 30)

#fig.tight_layout();
plt.savefig('Beta_x_.png', dpi = 800);

#############
#   Beta x  #
#############
print 'Plotting beta_x'
fig, ax1 = plt.subplots();

plt.title(r"PTC $\beta_x$");
if plot_610:
	if plot_LEQ: ax1.plot(leq_610_s, leq_610_betx, color='b', label=r'Q$_y$ = 6.10 LEQ')
	if plot_PFW: ax1.plot(pfw_610_s, pfw_610_betx, color='r', label=r'Q$_y$ = 6.10 PFW')
if plot_614:
	if plot_LEQ: ax1.plot(leq_614_s, leq_614_betx, color='m', label=r'Q$_y$ = 6.14 LEQ')
	if plot_PFW: ax1.plot(pfw_614_s, pfw_614_betx, color='orange', label=r'Q$_y$ = 6.14 PFW')
if plot_624:
	if plot_LEQ: ax1.plot(leq_624_s, leq_624_betx, color='k', label=r'Q$_y$ = 6.24 LEQ')
	if plot_PFW: ax1.plot(pfw_624_s, pfw_624_betx, color='c', label=r'Q$_y$ = 6.24 PFW')

ax1.set_xlabel("s [m]");
ax1.set_ylabel(r"$\beta_x$ [m]");

# Make the y-axis label, ticks and tick labels match the line color.
# ~ ax1.tick_params('y', colors='b');
#ax1.set_yscale('log')

ax1.set_xlim(0, xmax)
ax1.set_ylim(10, 30)

ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

ax1.legend(loc = 2);

#fig.tight_layout();
plt.savefig('Beta_x.png', dpi = 800);
    
#############
#   Beta y  #
#############
print 'Plotting beta_y'
fig, ax1 = plt.subplots();

plt.title(r"PTC $\beta_y$");

if plot_610:
	# ~ if plot_LEQ: ax1.plot(leq_610_s, leq_610_bety, color='b', label=r'Q$_y$ = 6.10 LEQ')
	if plot_LEQ: ax1.plot(leq_610_s, leq_610_bety, color='r', label=r'Q$_y$ = 6.10 LEQ')
	if plot_PFW: ax1.plot(pfw_610_s, pfw_610_bety, color='r', label=r'Q$_y$ = 6.10 PFW')
if plot_614:
	# ~ if plot_LEQ: ax1.plot(leq_614_s, leq_614_bety, color='m', label=r'Q$_y$ = 6.14 LEQ')
	if plot_LEQ: ax1.plot(leq_614_s, leq_614_bety, color='orange', label=r'Q$_y$ = 6.14 LEQ')
	if plot_PFW: ax1.plot(pfw_614_s, pfw_614_bety, color='orange', label=r'Q$_y$ = 6.14 PFW')
if plot_624:
	# ~ if plot_LEQ: ax1.plot(leq_624_s, leq_624_bety, color='k', label=r'Q$_y$ = 6.24 LEQ')
	if plot_LEQ: ax1.plot(leq_624_s, leq_624_bety, color='c', label=r'Q$_y$ = 6.24 LEQ')
	if plot_PFW: ax1.plot(pfw_624_s, pfw_624_bety, color='c', label=r'Q$_y$ = 6.24 PFW')

ax1.set_xlabel("s [m]");
ax1.set_ylabel(r"$\beta_y$ [m]");

# Make the y-axis label, ticks and tick labels match the line color.
# ~ ax1.tick_params('y', colors='b');
#ax1.set_yscale('log')

ax1.set_xlim(0, xmax)
ax1.set_ylim(10, 30)

ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

ax1.legend(loc = 2);

#fig.tight_layout();
plt.savefig('Beta_y.png', dpi = 800);
    
        
##############
#   Alpha x  #
##############
print 'Plotting alpha_x'
fig, ax1 = plt.subplots();

plt.title(r"PTC $\alpha_x$");
if plot_610:
	if plot_LEQ: ax1.plot(leq_610_s, leq_610_alfx, color='b', label=r'Q$_y$ = 6.10 LEQ')
	if plot_PFW: ax1.plot(pfw_610_s, pfw_610_alfx, color='r', label=r'Q$_y$ = 6.10 PFW')
if plot_614:
	if plot_LEQ: ax1.plot(leq_614_s, leq_614_alfx, color='m', label=r'Q$_y$ = 6.14 LEQ')
	if plot_PFW: ax1.plot(pfw_614_s, pfw_614_alfx, color='orange', label=r'Q$_y$ = 6.14 PFW')
if plot_624:
	if plot_LEQ: ax1.plot(leq_624_s, leq_624_alfx, color='k', label=r'Q$_y$ = 6.24 LEQ')
	if plot_PFW: ax1.plot(pfw_624_s, pfw_624_alfx, color='c', label=r'Q$_y$ = 6.24 PFW')

ax1.set_xlabel("s [m]");
ax1.set_ylabel(r"$\alpha_x$ [-]");

# Make the y-axis label, ticks and tick labels match the line color.
# ~ ax1.tick_params('y', colors='b');
#ax1.set_yscale('log')

ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

ax1.legend(loc = 2);
ax1.set_xlim(0, xmax)

#fig.tight_layout();
plt.savefig('Alpha_x.png', dpi = 800);

##############
#   Alpha y  #
##############
print 'Plotting alpha_y'
fig, ax1 = plt.subplots();

plt.title(r"PTC $\alpha_y$");
if plot_610:
	if plot_LEQ: ax1.plot(leq_610_s, leq_610_alfy, color='b', label=r'Q$_y$ = 6.10 LEQ')
	if plot_PFW: ax1.plot(pfw_610_s, pfw_610_alfy, color='r', label=r'Q$_y$ = 6.10 PFW')
if plot_614:
	if plot_LEQ: ax1.plot(leq_614_s, leq_614_alfy, color='m', label=r'Q$_y$ = 6.14 LEQ')
	if plot_PFW: ax1.plot(pfw_614_s, pfw_614_alfy, color='orange', label=r'Q$_y$ = 6.14 PFW')
if plot_624:
	if plot_LEQ: ax1.plot(leq_624_s, leq_624_alfy, color='k', label=r'Q$_y$ = 6.24 LEQ')
	if plot_PFW: ax1.plot(pfw_624_s, pfw_624_alfy, color='c', label=r'Q$_y$ = 6.24 PFW')

ax1.set_xlabel("s [m]");
ax1.set_ylabel(r"$\alpha_y$ [-]");

# Make the y-axis label, ticks and tick labels match the line color.
# ~ ax1.tick_params('y', colors='b');
#ax1.set_yscale('log')

ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

ax1.legend(loc = 2);
ax1.set_xlim(0, xmax)

#fig.tight_layout();
plt.savefig('Alpha_y.png', dpi = 800);


#################
#   Dispersion  #
#################
print 'Plotting D_x'
fig, ax1 = plt.subplots();

plt.title("PTC Dispersion Functions");
if plot_610:
	if plot_LEQ: ax1.plot(leq_610_s, leq_610_Dx, color='b', label=r'Q$_y$ = 6.10 LEQ')
	if plot_PFW: ax1.plot(pfw_610_s, pfw_610_Dx, color='r', label=r'Q$_y$ = 6.10 PFW')
if plot_614:
	if plot_LEQ: ax1.plot(leq_614_s, leq_614_Dx, color='m', label=r'Q$_y$ = 6.14 LEQ')
	if plot_PFW: ax1.plot(pfw_614_s, pfw_614_Dx, color='orange', label=r'Q$_y$ = 6.14 PFW')
if plot_624:
	if plot_LEQ: ax1.plot(leq_624_s, leq_624_Dx, color='k', label=r'Q$_y$ = 6.24 LEQ')
	if plot_PFW: ax1.plot(pfw_624_s, pfw_624_Dx, color='c', label=r'Q$_y$ = 6.24 PFW')

ax1.set_xlabel("s [m]");
ax1.set_ylabel(r"$D_x$ [m]");

# ~ ax1.tick_params('y', colors='b');

ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

ax1.legend(loc = 2);
ax1.set_xlim(0, xmax)
ax1.set_ylim(2, 4)

#fig.tight_layout();
plt.savefig('Dispersion_functions.png', dpi = 800);
