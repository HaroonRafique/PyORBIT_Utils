import matplotlib.pyplot as plt
import numpy as np

# Open File
pro_file='profile_PS_Injection_Slurm_1Node_plot.txt'

fin=open(pro_file,'r').readlines()[1:]

#   ncalls  tottime  percall  cumtime  percall filename:lineno(function) Nicename
ncalls =[]
tottime =[]
percall =[]
cumtime =[]
cumpercall =[]
function =[]
nicename =[]

# Read Data
for l in fin:  
    ncalls.append(float(l.split()[0]))
    tottime.append(float(l.split()[1]))
    percall.append(float(l.split()[2]))
    cumtime.append(float(l.split()[3]))
    cumpercall.append(float(l.split()[4]))
    function.append(str(l.split()[5])
    nicename.append(str(l.split()[6])


############
# Runtimes #
############

if(plot_runtimes):
    fig, ax1 = plt.subplots();

    
    ax1.pie(cumtime, labels=nicename, autopct='%1.1f%%', shadow=True)

    plt.title("Wall-clock runtimes for PyORBIT on HPC-Batch");
    ax1.plot(nodes, sec, 'b-', label='Runtime');

    ax1.set_xlabel("Nodes [-]");
    ax1.set_ylabel("Time [s]", color='b');
    ax1.tick_params('y', colors='b');
    #~ ax1.set_yscale('log')

    # ~ plt.xlim(100,300);
    #~ ax1.set_xlim(0,220);
    # ~ ax1.set_ylim(1.8E4, 2.8E4);
    ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
    ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)


    ax1.legend(loc = 2);

    fig.tight_layout();
    #~ plt.show();
    plt.savefig('test.png', dpi = 800);

