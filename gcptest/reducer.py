#!/usr/bin/env python
"""reducer.py"""

mut_map = {'Silent' : [],'Missense' : [] , 'Nonsense' : []}
transition = []
transversion = []
#print('Edit Mutations: \n')
#print('pos\torig\treplace')
transit_fd = open("Transitions.txt",'w')
transverse_fd = open("Transversions.txt",'w')
mutations_fd = open("Mutations.txt",'w')
bad_chars = ['(',')', ',','\'']
for line in sys.stdin:
    line = line.strip()
    for ctch in bad_chars:
        line = line.replace(ctch,"")
    splits = line.split("\t")

    mut_type = splits[0].strip()
    spits  = splits[1].strip()
    spits = spits.split()
    
    spits[0] = int(spits[0])
    #print(spits)
    tup = tuple(spits)
    #tup = (index,splits[2:])
    if mut_type == 'Transit' :
        transition.append(tup)
    elif mut_type == 'Transverse':
        transversion.append(tup)
    else:
        mut_map[mut_type].append(tup)
transition.sort()
if len(transition) != 0:
    for i in transition:
        transit_fd.write(str(i))
        transit_fd.write("\n")
else:
    transit_fd.write("No transitions found ")
transit_fd.close() 

transversion.sort()
if len(transversion) != 0:
    for i in transversion:
        transverse_fd.write(str(i))
        transverse_fd.write("\n")
else:
    transverse_fd.write("No transitions found ")
transverse_fd.close()

for i in mut_map:
    mut_map[i].sort()
    
for i,j in mut_map.items():
    mutations_fd.write(i)
    mutations_fd.write(":\n")
    for tup in j:
        mutations_fd.write(str(tup))
        mutations_fd.write("\n")
mutations_fd.close()
