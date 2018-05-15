import matplotlib.pyplot as plt
import numpy as np

# Open File
loss_file1='runtimes_PS_2p5d.txt'
loss_file2='runtimes_PS_2p5d_old.txt'


nodes1 = []
sec1 = []
threads1 = []
spernode1 = []
sperturn1 = []
sperthread1 = []
speedup1 = []

nodes2 = []
sec2 = []
threads2 = []
spernode2 = []
sperturn2 = []
sperthread2 = []
speedup2 = []

plot_runtimes = 1
plot_runtimes_log = 1
plot_runtimes_per_thread = 1
plot_runtimes_per_thread_log = 1
plot_runtimes_per_node = 1
plot_runtimes_per_node_log = 1
plot_speedup_cf_1node = 1
plot_speedup_cf_1thread = 1
plot_runtimes_per_turn = 1

# ~ firstLine1 = fin1.pop(0)
# ~ firstLine2 = fin2.pop(0)

Nturns = 100.

# Read Data
fin1=open(loss_file1,'r').readlines()[1:]
for l in fin1:  
    nodes1.append(float(l.split()[0]))
    sec1.append(abs(float(l.split()[1])))
    threads1.append(abs(float(l.split()[2])))
    spernode1.append(abs(float(l.split()[1]))/float(l.split()[0]))
    sperthread1.append(abs(float(l.split()[1]))/float(l.split()[2]))
    sperturn1.append(abs(float(l.split()[1])/Nturns))

fin2=open(loss_file2,'r').readlines()[1:]
for l in fin2:  
    nodes2.append(float(l.split()[0]))
    sec2.append(abs(float(l.split()[1])))
    threads2.append(abs(float(l.split()[2])))
    spernode2.append(abs(float(l.split()[1]))/float(l.split()[0]))
    sperthread2.append(abs(float(l.split()[1]))/float(l.split()[2]))
    sperturn2.append(abs(float(l.split()[1])/Nturns))

print '\nnodes = ', nodes1;
print '\nsec = ', sec1;
print '\nthreads = ', threads1;
print '\nspernode = ', spernode1;
print '\nsperthread = ', sperthread1;
print '\nsperturn = ', sperturn1;
print '\nnodes = ', nodes2;
print '\nsec = ', sec2;
print '\nthreads = ', threads2;
print '\nspernode = ', spernode2;
print '\nsperthread = ', sperthread2;
print '\nsperturn = ', sperturn2;


############
# Runtimes #
############

if(plot_runtimes):
    fig, ax1 = plt.subplots();

    plt.title("Wall-clock runtimes for PyORBIT on HPC-Batch");
    ax1.plot(nodes1, sec1, 'k-', label='Runtime 40thread Nodes');
    ax1.plot(nodes2, sec2, 'b-', label='Runtime 39thread Nodes');

    ax1.set_xlabel("Nodes [-]");
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
    ax2.plot(nodes1, spernode1, 'g:', label='Per CPU');
    ax2.plot(nodes2, spernode2, 'r:', label='Per CPU');
    ax2.set_ylabel('Time / Nodes [s]', color='r');
    ax2.tick_params('y', colors='r');
    #~ ax2.set_yscale('log')

    # ~ ax2.set_ylim(50,300);


    ax1.legend(loc = 2);
    ax2.legend(loc = 1);

    fig.tight_layout();
    #~ plt.show();
    plt.savefig('Runtimes.png', dpi = 800);

#######
# LOG #
#######

if (plot_runtimes_log):
    fig, ax1 = plt.subplots();

    plt.title("Wall-clock runtimes for PyORBIT on HPC-Batch logarithmic Y");
    ax1.plot(nodes1, sec1, 'k-', label='Runtime 40');
    ax1.plot(nodes2, sec2, 'b-', label='Runtime 39');
    ax1.set_yscale('log')
    ax2 = ax1.twinx();
    ax2.plot(nodes1, spernode1, 'g-', label='Per CPU 40');
    ax2.plot(nodes2, spernode2, 'r-', label='Per CPU 39');
    ax2.set_yscale('log')

    ax1.set_xlabel("Nodes [-]");
    ax1.set_ylabel("Time [s]", color='b');
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.tick_params('y', colors='b');
    ax1.yaxis.grid(color='b', which='minor', linestyle=':', linewidth=0.5)
    ax1.yaxis.grid(color='b', which='major', linestyle=':', linewidth=0.5)
    ax1.xaxis.grid(color='k',linestyle=':', linewidth=0.5)

    #~ ax1.set_xlim(0,220);
    # ~ ax1.set_ylim(1E4, 5E4);

    ax2.set_ylabel('Time / Nodes [s]', color='r');
    ax2.tick_params('y', colors='r');

    # ~ ax2.set_ylim(30,300);
    ax2.yaxis.grid(color='r', which='minor', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='r', which='major', linestyle=':', linewidth=0.5)

    ax1.legend(loc = 3);
    ax2.legend(loc = 1);

    fig.tight_layout();
    #~ plt.show();
    plt.savefig('Runtimes_log.png', dpi = 800);

#################
# time / thread #
#################
if (plot_runtimes_per_thread):

    fig, ax2 = plt.subplots();

    plt.title("Wall-clock runtimes per CPU for PyORBIT on HPC-Batch");

    #~ ax2 = ax1.twinx();
    ax2.plot(threads1, sperthread1, 'k-', label='Per thread 40');
    ax2.plot(threads2, sperthread2, 'r-', label='Per thread 39');
    
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
    fig, ax2 = plt.subplots();

    plt.title("Wall-clock runtimes per CPU for PyORBIT on HPC-Batch");

    #~ ax2 = ax1.twinx();
    ax2.plot(nodes1, spernode1, 'k-', label='Per node 40');
    ax2.plot(nodes2, spernode2, 'r-', label='Per node 39');
    ax2.set_xlabel("Nodes [-]", color='k');
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
    plt.savefig('Runtimes_time_per_node.png', dpi = 800);

###################
# time / node log #
###################
if (plot_runtimes_per_node_log):

    fig, ax2 = plt.subplots();

    plt.title("Wall-clock runtimes per CPU for PyORBIT on HPC-Batch");

    ax2.plot(nodes1, spernode1, 'k-', label='Per node 40');
    ax2.plot(nodes2, spernode2, 'r-', label='Per node 39');
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
    ax2.plot(threads1, sperthread1, 'k-', label='Per thread 40');
    ax2.plot(threads2, sperthread2, 'r-', label='Per thread 39');
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

    one_node1 = sec1[0]
    one_node2 = sec2[0]
    print '\none node1 = ', one_node1
    print '\none node2 = ', one_node2
    speedup1 = []
    speedup2 = []
    x=[]
    y=[]
    j=nodes1[0]
    for i in sec1:
        speedup1.append(one_node1/i)
        x.append(j)
        y.append(j)
        j += 1
    for i in sec2:
        speedup2.append(one_node2/i)

    print '\nSpeedup per node1 = ', speedup1
    print '\nSpeedup per node2 = ', speedup2
        
    fig, ax2 = plt.subplots();
    
    plt.title("Speedup factor per node \n(w.r.t. %i node = %1.2f s) \nfor PyORBIT on HPC-Batch" % (nodes1[0], one_node1));
    # ~ plt.title("Speedup factor per node (w.r.t. 1 node) for PyORBIT on HPC-Batch");

    #~ ax2 = ax1.twinx();
    ax2.plot(nodes1, speedup1, 'k-', label='Per Node 40');
    ax2.plot(nodes2, speedup2, 'r-', label='Per Node 39');
    ax2.plot(x, y, 'b:', label='Ideal');
    ax2.set_xlabel("Nodes [-]", color='k');
    ax2.set_ylabel("Speedup Factor [-]", color='k');
    #~ ax2.tick_params('y', colors='r');
    #~ ax2.set_yscale('log')

    #~ ax2.set_ylim(1E1,2E5);
    #~ ax2.yaxis.grid(color='r', which='minor', linestyle=':', linewidth=0.5)
    ax2.xaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='k', which='minor', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)

    ax2.legend(loc = 1);

    fig.tight_layout();
    #~ plt.show();
    plt.savefig('Speedup_per_node.png', dpi = 800);

######################
# speedup per thread #
######################
if (plot_speedup_cf_1thread):

    one_thread1 = sperthread1[0]
    one_thread2 = sperthread2[0]
    print '\none thread1 = ', one_thread1
    print '\none thread2= ', one_thread2
    speedup1 = []
    speedup2 = []

    for i in sperthread1:
        speedup1.append(one_thread1/i)
    for i in sperthread2:
        speedup2.append(one_thread2/i)

    print 'speedup per thread1 = ',speedup1
    print 'speedup per thread2 = ',speedup2
        
    fig, ax2 = plt.subplots();

    # print "1.000 + 1.000 = %1.3f" % num
    plt.title("Speedup factor per thread \n(w.r.t. %i node/%i threads = %1.2f s) \nfor PyORBIT on HPC-Batch" % (nodes1[0], threads1[0], one_thread1));

    #~ ax2 = ax1.twinx();
    ax2.plot(threads1, speedup1, 'k-', label='Per CPU 40');
    ax2.plot(threads2, speedup2, 'r-', label='Per CPU 39');
    ax2.set_xlabel("Threads [-]", color='k');
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
    plt.savefig('Speedup_per_thread.png', dpi = 800);

##############
# TURN #
##############
if (plot_runtimes_per_turn):

    fig, ax2 = plt.subplots();

    plt.title("Wall-clock runtimes per turn for PyORBIT on HPC-Batch");

    #~ ax2 = ax1.twinx();
    ax2.plot(nodes1, sperturn1, 'k-', label='Per CPU 40');
    ax2.plot(nodes2, sperturn2, 'r-', label='Per CPU 39');
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
