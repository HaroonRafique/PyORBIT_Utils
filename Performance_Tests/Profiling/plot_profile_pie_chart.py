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
    function.append(str(l.split()[5]))
    nicename.append(str(l.split()[6]))

D=dict()

# ~ print ncalls
print len(ncalls)

Tnicename=[]

# Sort etc
# First identify categories
for i in nicename:
    if i not in Tnicename:      # Add the new name if not already in existence
        Tnicename.append(i)
        D[i] = (0., 0., 0.)
print D


print nicename[0]

D2=dict()
D2tot=dict()

# Next increment ncalls, tottime, cumtime
# ~ it=len(ncalls)
for i in range(len(ncalls)):

    if nicename[i] in D2:        
        # ~ print 'Adding ', nicename[i], ' to D2'
        D2[nicename[i]]= (D2[nicename[i]][0]+ncalls[i],D2[nicename[i]][1]+tottime[i],D2[nicename[i]][2]+cumtime[i])
        # ~ print D2tot[nicename[i]]
        D2tot[nicename[i]]= D2tot[nicename[i]]+tottime[i]
    else:
        # ~ print 'Adding ', nicename[i], ' to D2'
        nc = ncalls[i] + D[nicename[i]][0]
        tt = tottime[i] + D[nicename[i]][1]
        ct = cumtime[i] + D[nicename[i]][2]
        D2[nicename[i]]= (nc,tt,ct)
        D2tot[nicename[i]]=tt

print D2tot

explode=[]
for i in D2tot:
    explode.append(0.1)

# ~ print D2.values()[:][2]

############
# Runtimes #
############

fig, ax1 = plt.subplots();

# ~ explode = 

plt.title("Profiling of PyORBIT on HPC-Batch 10 Turns");

ax1.pie(D2tot.values(), labels=D2tot.keys(), autopct='%0.01f%%', shadow=False, explode=explode, startangle=120)
# ~ ax1.pie(D2tot.values(), autopct='%0.1f%%', shadow=False, explode=explode, startangle=120)


# ~ ax1.legend(D2tot.values(), labels=D2tot.keys(), loc='left center', bbox_to_anchor=(-0.1, 1.), fontsize=8)
ax1.legend(D2tot.values(), labels=D2tot.keys(), loc=4, fontsize=8)

# ~ fig.tight_layout();
#~ plt.show();
plt.savefig('test.png', dpi = 800);

