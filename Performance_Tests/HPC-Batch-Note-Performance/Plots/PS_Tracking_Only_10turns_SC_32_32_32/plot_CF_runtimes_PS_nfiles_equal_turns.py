import matplotlib.pyplot as plt
import numpy as np
import sys
import os

def equate_turns(list1, list2, t1, t2):
    list_new=[]
    if t1 > t2:
        divisor = t1 / t2
        for i in list1:
            list_new.append(i/divisor)
        return (list_new, list2)
    elif t2 > t1:
        divisor = t2 / t1
        for i in list2:
            list_new.append(i/divisor)
        return (list1, list_new)
    elif t1 == t2:
        return (list1, list2)    
        
plot_runtimes = 1
plot_runtimes_log = 1
plot_speedup_cf_1node = 1
plot_runtimes_per_turn = 1

rootdir = os.getcwd()
extensions = ('.txt')

d = dict()
grid=''
Nturns=10

iterators = []

max_file_no = 0
min_file_no = 1E2
min_file=str()
max_file=str()

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext in extensions:
            print (os.path.join(subdir, file))      # full path to file
            grid = str(file.split('.')[0])          # SC gridsize
            iterators.append(grid)
            d[grid]={}                              # append empty grid to dictionary
            fin=open(file,'r').readlines()[1:]
            
            nodes=[]
            secs=[]
            threads=[]
            spernode=[]
            sperthread=[]
            sperturn=[]
            
            for l in fin:
                nodes.append(float(l.split()[0]))
                secs.append(float(l.split()[1]))
                threads.append(float(l.split()[2]))
                spernode.append(abs(float(l.split()[1]))/float(l.split()[0]))
                sperthread.append(abs(float(l.split()[1]))/float(l.split()[2]))
                sperturn.append(abs(float(l.split()[1])/Nturns))
                
            d[grid]['node']=nodes
            d[grid]['sec']=secs
            d[grid]['thread']=threads
            d[grid]['spernode']=spernode
            d[grid]['sperthread']=sperthread
            d[grid]['sperturn']=sperturn
    
# ~ for i in iterators:
    # ~ print d[i]
    # ~ print d[i]['sec']
    # ~ print d[i]['sec'][0]
    
############
# Runtimes #
############
if(plot_runtimes):
    fig, ax1 = plt.subplots();

    plt.title("Wall-clock runtimes for PyORBIT on HPC-Batch");

    plot_name = 'Runtimes_PerNode'    
    for i in iterators:
        labelin = str(i)
        ax1.plot(d[i]['node'], d[i]['sec'], label=i);
        plot_name = plot_name + '_cf_' + i

    plot_name = plot_name + '.png'

    ax1.set_xlabel("Nodes [-]");
    ax1.set_ylabel("Time [s]", color='b');
    ax1.tick_params('y', colors='b');

    ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
    ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

    ax1.legend(loc = 1);

    fig.tight_layout();
    plt.savefig(plot_name, dpi = 800);

####################
# Runtime per turn #
####################
if(plot_runtimes):
    fig, ax1 = plt.subplots();

    plt.title("Wall-clock runtimes for PyORBIT on HPC-Batch");

    plot_name = 'Runtimes_PerTurn'    
    for i in iterators:
        labelin = str(i)
        ax1.plot(d[i]['node'], d[i]['sperturn'], label=i);
        plot_name = plot_name + '_cf_' + i

    plot_name = plot_name + '.png'

    ax1.set_xlabel("Nodes [-]");
    ax1.set_ylabel("Time [s]", color='b');
    ax1.tick_params('y', colors='b');

    ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
    ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

    ax1.legend(loc = 1);

    fig.tight_layout();
    plt.savefig(plot_name, dpi = 800);

################
# Runtimes log #
################
if(plot_runtimes):
    fig, ax1 = plt.subplots();

    plt.title("Wall-clock runtimes for PyORBIT on HPC-Batch");

    plot_name = 'Runtimes_PerNode'    
    for i in iterators:
        labelin = str(i)
        ax1.plot(d[i]['node'], d[i]['sec'], label=i);
        plot_name = plot_name + '_cf_' + i

    plot_name = plot_name + '_log.png'

    ax1.set_xlabel("Nodes [-]");
    ax1.set_ylabel("Time [s]", color='b');
    ax1.tick_params('y', colors='b');

    ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
    ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)
    ax1.set_yscale('log')
    
    ax1.legend(loc = 1);

    fig.tight_layout();
    plt.savefig(plot_name, dpi = 800);


####################
# speedup per node #
####################
if (plot_speedup_cf_1node):
    
    fig, ax2 = plt.subplots();
    plt.title("Speedup factor per node \n(w.r.t. 1 node) \nfor PyORBIT on HPC-Batch")
    plot_name = 'Speedup_PerNode'  
    
    x=[]
    y=[]
    j =0
    while j < 10:
        x.append(j)
        y.append(j)
        j += 1       

    for i in iterators:
        plot_name = plot_name + '_cf_' + i
        one_node = d[i]['sec'][0]
        print '\none node = ', one_node
        speedup = []

        for j in (d[i]['sec']):
            speedup.append(one_node/j)

        ax2.plot(d[i]['node'], speedup, label=i);
        
    plot_name = plot_name + '.png'


    ax2.plot(x, y, 'r:', label='Ideal');
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
    plt.savefig(plot_name, dpi = 800);

    
sys.exit()

############
# Runtimes #
############
if(plot_runtimes):
    fig, ax1 = plt.subplots();

    plt.title("Wall-clock runtimes for PyORBIT on HPC-Batch");
    ax1.plot(nodes1, sec1, 'b-', label=label1);
    ax1.plot(nodes2, sec2, 'b:', label=label2);

    ax1.set_xlabel("Nodes [-]");
    ax1.set_ylabel("Time [s]", color='b');
    ax1.tick_params('y', colors='b');

    ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
    ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)

    ax2 = ax1.twinx()

    ax2label1 = 'Per Node' + label1
    ax2label2 = 'Per Node' + label2
    
    ax2.plot(nodes1, spernode1, 'r-', label=ax2label1);
    ax2.plot(nodes2, spernode2, 'r:', label=ax2label2);
    
    ax2.set_ylabel('Time / Nodes [s]', color='r');
    ax2.tick_params('y', colors='r');
    #~ ax2.set_yscale('log')

    # ~ ax2.set_ylim(50,300);


    ax1.legend(loc = 2);
    ax2.legend(loc = 1);

    fig.tight_layout();
    plot_name = 'Runtimes_+PerNode'+label1+'_cf_'+label2+'.png'
    plt.savefig(plot_name, dpi = 800);

###############
# Runtimes CF #
###############
if(plot_runtimes_cf):
    fig, ax1 = plt.subplots();

    plt.title("Wall-clock runtimes for PyORBIT on HPC-Batch");
    ax1.plot(nodes1, sec1, 'b-', label=label1);
    ax1.plot(nodes2, sec2, 'r-', label=label2);

    ax1.set_xlabel("Nodes [-]");
    ax1.set_ylabel("Time [s]", color='b');
    ax1.tick_params('y', colors='b');

    ax1.xaxis.grid(color='k', linestyle=':', linewidth=0.5)
    ax1.yaxis.grid(color='k', linestyle=':', linewidth=0.5)
    
    ax1.legend(loc = 2);

    fig.tight_layout();
    plot_name = 'Runtimes_'+label1+'_cf_'+label2+'.png'
    plt.savefig(plot_name, dpi = 800);


sys.exit()

#################
# time / thread #
#################
if (plot_runtimes_per_thread):

    fig, ax2 = plt.subplots();

    plt.title("Wall-clock runtimes per CPU for PyORBIT on HPC-Batch");

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
    fig, ax2 = plt.subplots();

    plt.title("Wall-clock runtimes per CPU for PyORBIT on HPC-Batch");

    #~ ax2 = ax1.twinx();
    ax2.plot(nodes, spernode, 'r-', label='Per node');
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

    #~ ax2.set_ylim(1E1,2E5);
    #~ ax2.yaxis.grid(color='r', which='minor', linestyle=':', linewidth=0.5)
    ax2.xaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='k', which='minor', linestyle=':', linewidth=0.5)
    ax2.yaxis.grid(color='k', which='major', linestyle=':', linewidth=0.5)

    ax2.legend(loc = 1);

    fig.tight_layout();
    #~ plt.show();
    plt.savefig('Speedup_per_node.png', dpi = 800);

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
    one_thread_100turns = one_thread_turn * 100
    
    # ~ one_thread = sperthread[0]
    one_thread = one_thread_100turns
    print '\none thread = ', one_thread
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
    ax2.plot(x, y1, 'b:', label='Ideal scaling with thread');
    # ~ ax2.plot(x, y2, 'g:', label='Ideal scaling per core');
    # ~ ax2.plot(x, y3, 'y:', label='Ideal scaling per thread');
    ax2.set_xlabel("Threads [-]", color='k');
    ax2.set_ylabel("Speedup Factor [-]", color='k');
    #~ ax2.tick_params('y', colors='r');
    #~ ax2.set_yscale('log')

    #~ ax2.set_ylim(1E1,2E5);
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
