import matplotlib.pyplot as plt
import numpy as np

# Open File
loss_file='runtimes_PS_2p5d.txt'

fin=open(loss_file,'r').readlines()

i = 0
cpus = []
sec = []
sperc = []
speedup = []
sperturn = []

firstLine = fin.pop(0)

Nturns = 1000.

# Read Data
for l in fin:  
    cpus.append(float(l.split()[0])/2)
    sec.append(abs(float(l.split()[1])))
    sperc.append(abs(float(l.split()[1]))/float(l.split()[0]))
    sperturn.append(abs(float(l.split()[1])/Nturns))
    speedup.append(float(250000.)/float(l.split()[1]))

print 'cpus = ', cpus;
print 'sec = ', sec;
print 's/c = ', sperc;
print 'speedup = ', speedup;

fig, ax1 = plt.subplots();

plt.title("Wall-clock runtimes for PyORBIT on HPC-Batch");
ax1.plot(cpus, sec, 'b-', label='Runtime');

ax1.set_xlabel("CPUs [-]");
ax1.set_ylabel("Time [s]", color='b');
# Make the y-axis label, ticks and tick labels match the line color.
ax1.tick_params('y', colors='b');
#~ ax1.set_yscale('log')

# ~ plt.xlim(100,300);
#~ ax1.set_xlim(0,220);
# ~ ax1.set_ylim(1.8E4, 2.8E4);
ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

ax2 = ax1.twinx();
ax2.plot(cpus, sperc, 'r-', label='Per CPU');
ax2.set_ylabel('Time / CPU [s]', color='r');
ax2.tick_params('y', colors='r');
#~ ax2.set_yscale('log')

# ~ ax2.set_ylim(50,300);


ax1.legend(loc = 2);
ax2.legend(loc = 1);

fig.tight_layout();
#~ plt.show();
plt.savefig('Runtimes_PS.png', dpi = 800);


#######
# LOG #
#######

fig, ax1 = plt.subplots();

plt.title("Wall-clock runtimes for PyORBIT on HPC-Batch logarithmic Y");
ax1.plot(cpus, sec, 'b-', label='Runtime');
ax1.set_yscale('log')
ax2 = ax1.twinx();
ax2.plot(cpus, sperc, 'r-', label='Per CPU');
ax2.set_yscale('log')

ax1.set_xlabel("CPUs [-]");
ax1.set_ylabel("Time [s]", color='b');
# Make the y-axis label, ticks and tick labels match the line color.
ax1.tick_params('y', colors='b');
ax1.yaxis.grid(color='b', which='minor', linestyle=':', linewidth=0.5)
ax1.yaxis.grid(color='b', which='major', linestyle=':', linewidth=0.5)
ax1.xaxis.grid(color='k',linestyle=':', linewidth=0.5)

#~ ax1.set_xlim(0,220);
ax1.set_ylim(1E4, 5E4);

ax2.set_ylabel('Time / CPU [s]', color='r');
ax2.tick_params('y', colors='r');

# ~ ax2.set_ylim(30,300);
ax2.yaxis.grid(color='r', which='minor', linestyle=':', linewidth=0.5)
ax2.yaxis.grid(color='r', which='major', linestyle=':', linewidth=0.5)

ax1.legend(loc = 3);
ax2.legend(loc = 1);

fig.tight_layout();
#~ plt.show();
plt.savefig('Runtimes_log_PS.png', dpi = 800);

##############
# time / CPU #
##############

fig, ax2 = plt.subplots();

plt.title("Wall-clock runtimes per CPU for PyORBIT on HPC-Batch");

#~ ax2 = ax1.twinx();
ax2.plot(cpus, sperc, 'r-', label='Per CPU');
ax2.set_xlabel("CPUs [-]", color='k');
ax2.set_ylabel("Time [s]", color='k');
#~ ax2.tick_params('y', colors='r');
#~ ax2.set_yscale('log')

# ~ ax1.set_ylim(1.8E4, 2.8E4);
#~ ax2.yaxis.grid(color='r', which='minor', linestyle=':', linewidth=0.5)
ax2.xaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)
ax2.yaxis.grid(color='k', which='minor', linestyle=':', linewidth=0.5)
ax2.yaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)

fig.tight_layout();
#~ plt.show();
plt.savefig('Runtimes_time_per_cpu_PS.png', dpi = 800);

##################
# time / CPU log #
##################

fig, ax2 = plt.subplots();

plt.title("Wall-clock runtimes per CPU for PyORBIT on HPC-Batch");

#~ ax2 = ax1.twinx();
ax2.plot(cpus, sperc, 'r-', label='Per CPU');
ax2.set_xlabel("CPUs [-]", color='k');
ax2.set_ylabel("Time [s]", color='k');
#~ ax2.tick_params('y', colors='r');
ax2.set_yscale('log')

# ~ ax2.set_ylim(1E1,2E5);
#~ ax2.yaxis.grid(color='r', which='minor', linestyle=':', linewidth=0.5)
ax2.xaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)
ax2.yaxis.grid(color='k', which='minor', linestyle=':', linewidth=0.5)
ax2.yaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)

fig.tight_layout();
#~ plt.show();
plt.savefig('Runtimes_time_per_cpu_log_PS.png', dpi = 800);

###########
# speedup #
###########

fig, ax2 = plt.subplots();

plt.title("Speedup factor per CPU (w.r.t. estimate on 1 CPU) for PyORBIT on HPC-Batch");

#~ ax2 = ax1.twinx();
ax2.plot(cpus, speedup, 'r-', label='Per CPU');
ax2.set_xlabel("CPUs [-]", color='k');
ax2.set_ylabel("Speedup Factor [-]", color='k');
#~ ax2.tick_params('y', colors='r');
#~ ax2.set_yscale('log')

#~ ax2.set_ylim(1E1,2E5);
#~ ax2.yaxis.grid(color='r', which='minor', linestyle=':', linewidth=0.5)
ax2.xaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)
ax2.yaxis.grid(color='k', which='minor', linestyle=':', linewidth=0.5)
ax2.yaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)

fig.tight_layout();
#~ plt.show();
plt.savefig('Speedup_per_cpu_PS.png', dpi = 800);

###############
# speedup log #
###############

# ~ fig, ax2 = plt.subplots();

# ~ plt.title("Speedup factor per CPU (c.f. estimate on 1 CPU) for PyORBIT on HPC-Batch");

# ~ ax2.plot(cpus, speedup, 'r-', label='Per CPU');
# ~ ax2.set_xlabel("CPUs [-]", color='k');
# ~ ax2.set_ylabel("Speedup Factor [-]", color='k');
# ~ ax2.set_yscale('log')

# ~ ax2.xaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)
# ~ ax2.yaxis.grid(color='k', which='minor', linestyle=':', linewidth=0.5)
# ~ ax2.yaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)

# ~ fig.tight_layout();
# ~ plt.savefig('Speedup_per_cpu_log_PS.png', dpi = 800);


##############
# TURN #
##############

fig, ax2 = plt.subplots();

plt.title("Wall-clock runtimes per turn for PyORBIT on HPC-Batch");

#~ ax2 = ax1.twinx();
ax2.plot(cpus, sperturn, 'r-', label='Per CPU');
ax2.set_xlabel("CPUs [-]", color='k');
ax2.set_ylabel("Time for 1 turn [s]", color='k');
#~ ax2.tick_params('y', colors='r');
#~ ax2.set_yscale('log')

# ~ ax2.set_ylim(1E1,1.4E5);
#~ ax2.yaxis.grid(color='r', which='minor', linestyle=':', linewidth=0.5)
ax2.xaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)
ax2.yaxis.grid(color='k', which='minor', linestyle=':', linewidth=0.5)
ax2.yaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)

fig.tight_layout();
#~ plt.show();
plt.savefig('Runtimes_time_per_turn_PS.png', dpi = 800);
