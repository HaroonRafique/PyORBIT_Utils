import matplotlib.pyplot as plt
import numpy as np
import sys

# Open File
loss_file='runtimes_PS_2p5d.txt'

fin=open(loss_file,'r').readlines()

nodes = []
sec = []
threads = []
spernode = []
sperturn = []
sperthread = []
speedup = []

plot_runtimes = 1
plot_runtimes_log = 1
plot_runtimes_per_thread = 0
plot_runtimes_per_thread_log = 0
plot_runtimes_per_node = 1
plot_runtimes_per_node_log = 0
plot_speedup_cf_1node = 1
plot_speedup_cf_1thread = 1
plot_speedup_cf_1cpu = 1
plot_runtimes_per_turn = 1
plot_runtimes_per_turn_HTC = 1

firstLine = fin.pop(0)

Nturns = 100.

# Read Data
for l in fin:  
    nodes.append(float(l.split()[0]))
    sec.append(abs(float(l.split()[1])))
    threads.append(abs(float(l.split()[2])))
    spernode.append(abs(float(l.split()[1]))/float(l.split()[0]))
    sperthread.append(abs(float(l.split()[1]))/float(l.split()[2]))
    sperturn.append(abs(float(l.split()[1])/Nturns))

print '\nnodes = ', nodes;
print '\nsec = ', sec;
print '\nthreads = ', threads;
print '\nspernode = ', spernode;
print '\nsperthread = ', sperthread;
print '\nsperturn = ', sperturn;


# Open File
loss_file_htc='runtimes_PS_2p5d_HTC.txt'

htcfin=open(loss_file_htc,'r').readlines()[1:]

cpus_H=[]
sec_H = []
spercpu_H = []
sperturn_H = []
speedup_H = []

firstLine = fin.pop(0)

Nturns = 100.

# Read Data
for l in htcfin:  
    cpus_H.append(float(l.split()[0]))
    sec_H.append(abs(float(l.split()[1])))
    spercpu_H.append(abs(float(l.split()[1]))/float(l.split()[0]))
    sperturn_H.append(abs(float(l.split()[1])/Nturns))


############
# Runtimes #
############

if(plot_runtimes):
    fig, ax1 = plt.subplots();

    plt.title("Wall-clock runtimes for PyORBIT on HPC-Batch");
    ax1.plot(nodes, sec, 'b-', label='SLURM');
    ax1.plot(cpus_H, sec_H, 'r-', label='CONDOR');

    ax1.set_xlabel("Nodes or CPUs [-]");
    ax1.set_ylabel("Time [s]", color='b');
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.tick_params('y', colors='b');
    #~ ax1.set_yscale('log')

    # ~ plt.xlim(100,300);
    #~ ax1.set_xlim(0,220);
    # ~ ax1.set_ylim(1.8E4, 2.8E4);
    ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
    ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

    # ~ ax2 = ax1.twinx();
    # ~ ax2.plot(nodes, spernode, 'r-', label='Per CPU');
    # ~ ax2.set_ylabel('Time [s]', color='r');
    # ~ ax2.tick_params('y', colors='r');
    #~ ax2.set_yscale('log')

    # ~ ax2.set_ylim(50,300);


    ax1.legend(loc = 2);
    # ~ ax2.legend(loc = 1);

    fig.tight_layout();
    #~ plt.show();
    plt.savefig('Runtimes.png', dpi = 800);
    
############
# Runtimes #
############

if(plot_runtimes):
    fig, ax1 = plt.subplots();

    plt.title("Wall-clock runtimes for PyORBIT on HPC-Batch");
    ax1.plot(threads, sec, 'b-', label='SLURM');
    ax1.plot(cpus_H, sec_H, 'r-', label='CONDOR');

    ax1.set_xlabel("Threads or Cores [-]");
    ax1.set_ylabel("Time [s]", color='b');
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.tick_params('y', colors='b');
    #~ ax1.set_yscale('log')

    # ~ plt.xlim(100,300);
    #~ ax1.set_xlim(0,220);
    # ~ ax1.set_ylim(1.8E4, 2.8E4);
    ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
    ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

    # ~ ax2 = ax1.twinx();
    # ~ ax2.plot(nodes, spernode, 'r-', label='Per CPU');
    # ~ ax2.set_ylabel('Time [s]', color='r');
    # ~ ax2.tick_params('y', colors='r');
    #~ ax2.set_yscale('log')

    # ~ ax2.set_ylim(50,300);


    ax1.legend(loc = 2);
    # ~ ax2.legend(loc = 1);

    fig.tight_layout();
    #~ plt.show();
    plt.savefig('Thread_Runtimes.png', dpi = 800);

#######
# LOG #
#######

# ~ if (plot_runtimes_log):
    # ~ fig, ax1 = plt.subplots();

    # ~ plt.title("Wall-clock runtimes for PyORBIT on HPC-Batch logarithmic Y");
    # ~ ax1.plot(nodes, sec, 'b-', label='Runtime');
    # ~ ax1.set_yscale('log')
    # ~ ax2 = ax1.twinx();
    # ~ ax2.plot(nodes, spernode, 'r-', label='Per CPU');
    # ~ ax2.set_yscale('log')

    # ~ ax1.set_xlabel("Nodes [-]");
    # ~ ax1.set_ylabel("Time [s]", color='b');
    # ~ # Make the y-axis label, ticks and tick labels match the line color.
    # ~ ax1.tick_params('y', colors='b');
    # ~ ax1.yaxis.grid(color='b', which='minor', linestyle=':', linewidth=0.5)
    # ~ ax1.yaxis.grid(color='b', which='major', linestyle=':', linewidth=0.5)
    # ~ ax1.xaxis.grid(color='k',linestyle=':', linewidth=0.5)

    # ~ ax2.set_ylabel('Time / Nodes [s]', color='r');
    # ~ ax2.tick_params('y', colors='r');

    # ~ ax2.yaxis.grid(color='r', which='minor', linestyle=':', linewidth=0.5)
    # ~ ax2.yaxis.grid(color='r', which='major', linestyle=':', linewidth=0.5)

    # ~ ax1.legend(loc = 3);
    # ~ ax2.legend(loc = 1);

    # ~ fig.tight_layout();
    # ~ #~ plt.show();
    # ~ plt.savefig('Runtimes_log.png', dpi = 800);

#################
# time / thread #
#################
if (plot_runtimes_per_thread):

    fig, ax2 = plt.subplots();

    plt.title("Wall-clock runtimes per thread for PyORBIT on HPC-Batch");

    #~ ax2 = ax1.twinx();
    ax2.plot(threads, sperthread, 'r-', label='Per thread');
    ax2.set_xlabel("Threads [-]", color='k');
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
    plt.savefig('Runtimes_time_per_thread.png', dpi = 800);


#################
# time / node #
#################
if (plot_runtimes_per_node):
    fig, ax1 = plt.subplots();

    plt.title("Wall-clock runtimes per Node for PyORBIT on HPC-Batch");

    #~ ax2 = ax1.twinx();
    ax1.plot(nodes, spernode, 'r-', label='Per node');
    ax1.set_xlabel("Nodes [-]", color='k');
    ax1.set_ylabel("Time [s]", color='k');
    #~ ax2.tick_params('y', colors='r');
    #~ ax2.set_yscale('log')

    # ~ ax1.set_ylim(1.8E4, 2.8E4);
    #~ ax2.yaxis.grid(color='r', which='minor', linestyle=':', linewidth=0.5)
    ax1.xaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)
    ax1.yaxis.grid(color='k', which='minor', linestyle=':', linewidth=0.5)
    ax1.yaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)

    fig.tight_layout();
    #~ plt.show();
    plt.savefig('Runtimes_time_per_node.png', dpi = 800);

    fig, ax2 = plt.subplots();

    plt.title("Wall-clock runtimes per CPU for PyORBIT on HPC-Batch");

    #~ ax2 = ax1.twinx();
    ax2.plot(cpus_H, spercpu_H, 'r-', label='Per CPU');
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
    plt.savefig('Runtimes_time_per_CPU.png', dpi = 800);

# ~ sys.exit()

###################
# time / node log #
###################
if (plot_runtimes_per_node_log):

    fig, ax2 = plt.subplots();

    plt.title("Wall-clock runtimes per CPU for PyORBIT on HPC-Batch");

    ax2.plot(nodes, spernode, 'r-', label='Per node');
    ax2.set_xlabel("Nodes [-]", color='k');
    ax2.set_ylabel("Time [s]", color='k');
    ax2.set_yscale('log')

    ax2.xaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='k', which='minor', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)

    fig.tight_layout();
    plt.savefig('Runtimes_time_per_node_log.png', dpi = 800);


#####################
# time / thread log #
#####################
if (plot_runtimes_per_thread_log):

    fig, ax2 = plt.subplots();

    plt.title("Wall-clock runtimes per CPU for PyORBIT on HPC-Batch");

    #~ ax2 = ax1.twinx();
    ax2.plot(threads, sperthread, 'r-', label='Per thread');
    ax2.set_xlabel("Threads [-]", color='k');
    ax2.set_ylabel("Time [s]", color='k');
    ax2.set_yscale('log')
    
    # ~ ax1.set_ylim(1.8E4, 2.8E4);
    #~ ax2.yaxis.grid(color='r', which='minor', linestyle=':', linewidth=0.5)
    ax2.xaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='k', which='minor', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)

    fig.tight_layout();
    #~ plt.show();
    plt.savefig('Runtimes_time_per_thread_log.png', dpi = 800);

####################
# speedup per node #
####################
if (plot_speedup_cf_1node):

    one_node = sec[0]
    print '\none node = ', one_node
    speedup = []
    x=[]
    y=[]
    j=nodes[0]
    for i in sec:
        speedup.append(one_node/i)
        x.append(j)
        y.append(j)
        j += 1

    # ~ print '\nSpeedup per node = ', speedup
        
    fig, ax2 = plt.subplots();
    
    plt.title("Speedup factor per node \n(w.r.t. %i node = %1.2f s) \nfor PyORBIT on HPC-Batch" % (nodes[0], one_node));
    # ~ plt.title("Speedup factor per node (w.r.t. 1 node) for PyORBIT on HPC-Batch");

    #~ ax2 = ax1.twinx();
    ax2.plot(nodes, speedup, 'r-', label='Per CPU');
    ax2.plot(x, y, 'b:', label='Ideal');
    ax2.set_xlabel("Nodes [-]", color='k');
    ax2.set_ylabel("Speedup Factor [-]", color='k');
    #~ ax2.tick_params('y', colors='r');
    #~ ax2.set_yscale('log')

    ax2.set_ylim(0,10);
    #~ ax2.yaxis.grid(color='r', which='minor', linestyle=':', linewidth=0.5)
    ax2.xaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='k', which='minor', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)

    ax2.legend(loc = 1);

    fig.tight_layout();
    #~ plt.show();
    plt.savefig('Speedup_per_node.png', dpi = 800);
    
####################
# speedup per CPU  #
####################
if (plot_speedup_cf_1cpu):

    one_cpu = sec_H[0]
    print '\none cpu = ', one_cpu
    speedup = []
    x=[]
    y=[]
    j=cpus_H[0]
    for i in sec_H:
        speedup.append(one_cpu/i)

    for j in cpus_H:
        x.append(j)
        y.append(j)

    # ~ print '\nSpeedup per node = ', speedup
        
    fig, ax2 = plt.subplots();
    
    plt.title("Speedup factor per cpu \n(w.r.t. %i CPU = %1.2f s) \nfor PyORBIT on HPC-Batch" % (cpus_H[0], one_cpu));
    # ~ plt.title("Speedup factor per node (w.r.t. 1 node) for PyORBIT on HPC-Batch");

    #~ ax2 = ax1.twinx();
    ax2.plot(cpus_H, speedup, 'r-', label='Per CPU');
    # ~ ax2.plot(x, y, 'b:', label='Ideal');
    ax2.set_xlabel("CPUs [-]", color='k');
    ax2.set_ylabel("Speedup Factor [-]", color='k');
    #~ ax2.tick_params('y', colors='r');
    #~ ax2.set_yscale('log')

    ax2.set_ylim(0,10);
    #~ ax2.yaxis.grid(color='r', which='minor', linestyle=':', linewidth=0.5)
    ax2.xaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='k', which='minor', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)

    ax2.legend(loc = 1);

    fig.tight_layout();
    #~ plt.show();
    plt.savefig('Speedup_per_cpu.png', dpi = 800);

###########################
# speedup per node turn #
###########################
if (plot_speedup_cf_1thread):

    # ~ one_node_turn = 558
    one_node_turn = sperturn[0]
    one_node = one_node_turn
    
    speedup = []
    x=[]
    y=[]
    j=1
    
    for i in sperturn:
        speedup.append(one_node/i)
        x.append(j)                  # threads at steps of each node
        y.append(j)                  # linear scaling with threads 
        j += 1

    print '\nspeedup per node turn = ',speedup
    
    fig, ax2 = plt.subplots();
    
    plt.title("Speedup factor per thread \n(w.r.t. 1 threads = %1.2f s) \nfor PyORBIT on HPC-Batch" % (one_node));

    ax2.plot(nodes, speedup, 'r-', label='Per CPU');
    ax2.plot(x, y, 'b:', label='Ideal scaling with node');
    
    ax2.set_xlabel("Threads [-]", color='k');
    ax2.set_ylabel("Speedup Factor [-]", color='k');
    
    ax2.xaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='k', which='minor', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)
    ax2.legend();
    
    fig.tight_layout();
    #~ plt.show();
    plt.savefig('Speedup_per_nodeturn.png', dpi = 800);

###########################
# speedup per thread turn #
###########################
if (plot_speedup_cf_1thread):

    one_thread_turn = 558
    one_thread = one_thread_turn
    
    speedup = []
    x=[]
    y=[]
    j=1

    new_sperturn=[]
    new_threads=[]
    new_threads.append(1)
    new_sperturn.append(one_thread)
    
    for i in sperturn:
        new_sperturn.append(i)
    for i in threads:
        new_threads.append(i)

    x.append(1)
    y.append(1)
    
    for i in new_sperturn:
        speedup.append(one_thread/i)
        x.append(j*40)                  # threads at steps of each node
        y.append(j*40)                  # linear scaling with threads 
        j += 1

    # ~ print '\nspeedup per thread = ',speedup
    
    fig, ax2 = plt.subplots();
    
    plt.title("Speedup factor per thread \n(w.r.t. 1 threads = %1.2f s) \nfor PyORBIT on HPC-Batch" % (one_thread));

    ax2.plot(new_threads, speedup, 'r-', label='Per CPU');
    ax2.plot(x, y, 'b:', label='Ideal scaling with thread');
    
    ax2.set_xlabel("Threads [-]", color='k');
    ax2.set_ylabel("Speedup Factor [-]", color='k');
    
    ax2.xaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='k', which='minor', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)
    ax2.legend();
    
    fig.tight_layout();
    #~ plt.show();
    plt.savefig('Speedup_per_threadturn.png', dpi = 800);

######################
# speedup per thread #
######################
if (plot_speedup_cf_1thread):

    one_thread_turn = 558
    # ~ one_thread_100turns = one_thread_turn * 100
    one_thread_100turns = one_thread_turn
    
    # ~ one_thread = sperthread[0]
    one_thread = one_thread_100turns
    print '\none thread = ', one_thread
    print '\sperturn = ', new_sperturn[0]
    speedup = []
    x=[]
    y1=[]
    y2=[]
    y3=[]
    j=1

    new_sperthread=[]
    new_sperturn=[]
    new_threads=[]
    new_threads.append(1)
    new_sperthread.append(one_thread_100turns)
    new_sperturn.append(one_thread_100turns)
    
    for i in sperthread:
        new_sperthread.append(i)
    for i in sperturn:
        new_sperturn.append(i)
    for i in threads:
        new_threads.append(i)

    x.append(1)
    y1.append(1)
    y2.append(1)
    y3.append(1)
    
    for i in new_sperturn:
        speedup.append(one_thread/i)
        x.append(j*40)                  # threads at steps of each node
        y1.append((one_thread / j*40)/(one_thread/i)) # linear scaling with threads 
        # ~ y2.append(j*40*20)              # linear scaling with nodes
        # ~ y3.append(j*40)                 # linear scaling with threads
        j += 1

    # ~ print 'speedup per thread = ',speedup
    print y1
    
    fig, ax2 = plt.subplots();

    # print "1.000 + 1.000 = %1.3f" % num
    plt.title("Speedup factor per thread \n(w.r.t. 1 threads = %1.2f s) \nfor PyORBIT on HPC-Batch" % (one_thread_100turns));

    #~ ax2 = ax1.twinx();
    ax2.plot(new_threads, speedup, 'r-', label='Per CPU');
    # ~ ax2.plot(x, y1, 'b:', label='Ideal scaling with thread');
    # ~ ax2.plot(x, y2, 'g:', label='Ideal scaling per core');
    # ~ ax2.plot(x, y3, 'y:', label='Ideal scaling per thread');
    ax2.set_xlabel("Threads [-]", color='k');
    ax2.set_ylabel("Speedup Factor [-]", color='k');
    #~ ax2.tick_params('y', colors='r');
    #~ ax2.set_yscale('log')

    ax2.set_xlim(0,16);
    ax2.set_ylim(0,10);
    #~ ax2.yaxis.grid(color='r', which='minor', linestyle=':', linewidth=0.5)
    ax2.xaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='k', which='minor', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)
    ax2.legend();
    
    fig.tight_layout();
    #~ plt.show();
    plt.savefig('Speedup_per_thread.png', dpi = 800);

##############
# TURN #
##############
if (plot_runtimes_per_turn):

    fig, ax2 = plt.subplots();

    plt.title("Wall-clock runtimes per turn for PyORBIT on HPC-Batch");

    #~ ax2 = ax1.twinx();
    ax2.plot(nodes, sperturn, 'r-', label='Per CPU');
    ax2.set_xlabel("Nodes [-]", color='k');
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
    plt.savefig('Runtimes_time_per_turn.png', dpi = 800);
    
##############
# TURN #
##############
if (plot_runtimes_per_turn_HTC):

    fig, ax2 = plt.subplots();

    plt.title("Wall-clock runtimes per turn for PyORBIT on HPC-Batch");

    #~ ax2 = ax1.twinx();
    ax2.plot(cpus_H, sperturn_H, 'r-', label='Per CPU');
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
    plt.savefig('Runtimes_time_per_turn_HTC.png', dpi = 800);
