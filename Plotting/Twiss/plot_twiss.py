import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['figure.figsize'] = [8.0, 6.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.rcParams['font.size'] = 6
plt.rcParams['legend.fontsize'] = 'small'
plt.rcParams['figure.titlesize'] = 'medium'

plt.rcParams['lines.linewidth'] = 0.5

# Open Files

ptc_file='ptc_twiss'
sis18_file='twiss-sis18'

fin1=open(sis18_file,'r').readlines()[8:]
# ~ firstLine = fin1.pop(8)

s18 = []
betx18 = []
bety18 = []
dx18 = []
dxp18 = []
mux18 = []
muy18 = []

s = []
betx = []
bety = []
dx = []
dxp = []
mux = []
muy = []

plot_betax = 1
plot_betay = 1
plot_dx = 1
plot_dxp = 1
plot_mux = 1
plot_muy = 1

beta = 0.15448

# Read Data
for l in fin1:
    s18.append(float(l.split()[3]))
    betx18.append(float(l.split()[4]))
    bety18.append(float(l.split()[11]))
    dx18.append(float(l.split()[9]))
    dxp18.append(float(l.split()[10]))
    mux18.append(float(l.split()[6]))
    muy18.append(float(l.split()[13]))

fin2=open(ptc_file,'r').readlines()[47:]
for f in fin2:
    s.append(float(f.split()[2]))
    betx.append(float(f.split()[6]))
    bety.append(float(f.split()[7]))
    dx.append(float(f.split()[12])*beta)
    dxp.append(float(f.split()[14])*beta)
    # ~ mux.append(float(l.split[6]))
    # ~ muy.append(float(l.split[13]))

############
#   Betas  #
############

if(plot_betax):
    fig, ax1 = plt.subplots();

    plt.title("SIS18 Beta_x");
    ax1.plot(s18, betx18, 'k-', label='SIS18 Beta_x', linewidth=1.5);
    ax1.plot(s, betx, 'r:', label='PTC Beta_x', linewidth=1.5);

    ax1.set_xlabel("s [m]");
    ax1.set_ylabel("Beta [m]", color='b');
    ax1.plot(s18, bety18, 'g-', label='SIS18 Beta_y', linewidth=1.5);
    ax1.plot(s, bety, 'b:', label='PTC Beta_y', linewidth=1.5);
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.tick_params('y', colors='b');
    ax1.set_yscale('log')

    # ~ plt.xlim(100,300);
    #~ ax1.set_xlim(0,220);
    # ~ ax1.set_ylim(1.8E4, 2.8E4);
    ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
    ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

    # ~ ax2 = ax1.twinx();
    # ~ ax2.set_ylabel("Beta [m]", color='r');
    # ~ ax2.tick_params('y', colors='r');
    #~ ax2.set_yscale('log')

    # ~ ax2.set_ylim(50,300);


    ax1.legend(loc = 2);
    # ~ ax2.legend(loc = 1);

    fig.tight_layout();
    #~ plt.show();
    plt.savefig('Betas.png', dpi = 800);

#################
#   Dispersion  #
#################

if(plot_betax):
    fig, ax1 = plt.subplots();

    plt.title("SIS18 D_x");
    ax1.plot(s18, dx18, 'k-', label='SIS18 Dx', linewidth=1.5);
    # ~ ax1.plot(s, dx, 'r:', label='PTC Beta_x', linewidth=1.5);
    ax1.set_xlabel("s [m]");
    ax1.set_ylabel("D [m]", color='b');
    
    ax1.tick_params('y', colors='b');
    # ~ ax1.set_yscale('log')

    # ~ ax1.set_ylim(1.8E4, 2.8E4);
    ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
    ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

    ax2 = ax1.twinx();
    # ~ ax1.plot(s18, dx18, 'k-', label='SIS18 Beta_x', linewidth=1.5);   
    ax2.plot(s, dx, 'r:', label='PTC Dx', linewidth=1.5);
    ax2.set_ylabel("D [m]", color='r');
    ax2.tick_params('y', colors='r');
    #~ ax2.set_yscale('log')

    # ~ ax2.set_ylim(50,300);


    ax1.legend(loc = 2);
    ax2.legend(loc = 1);

    fig.tight_layout();
    #~ plt.show();
    plt.savefig('Dx.png', dpi = 800);


#################
# Chromaticity  #
#################

if(plot_betax):
    fig, ax1 = plt.subplots();

    plt.title("SIS18 Dxp");
    ax1.plot(s18, dxp18, 'k-', label='SIS18 Dx', linewidth=1.5);
    # ~ ax1.plot(s, dx, 'r:', label='PTC Beta_x', linewidth=1.5);
    ax1.set_xlabel("s [m]");
    ax1.set_ylabel("D' [-]", color='b');
    
    ax1.tick_params('y', colors='b');
    # ~ ax1.set_yscale('log')

    # ~ ax1.set_ylim(1.8E4, 2.8E4);
    ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
    ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

    ax2 = ax1.twinx();
    # ~ ax1.plot(s18, dx18, 'k-', label='SIS18 Beta_x', linewidth=1.5);   
    ax2.plot(s, dxp, 'r:', label='PTC Dx', linewidth=1.5);
    ax2.set_ylabel("D' [-]", color='r');
    ax2.tick_params('y', colors='r');
    #~ ax2.set_yscale('log')

    # ~ ax2.set_ylim(50,300);


    ax1.legend(loc = 2);
    ax2.legend(loc = 1);

    fig.tight_layout();
    #~ plt.show();
    plt.savefig('Dxp.png', dpi = 800);
