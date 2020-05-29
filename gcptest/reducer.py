#!/usr/bin/env python
"""reducer.py"""
"""
from operator import itemgetter
import sys

word_map = {}
"""
bad_chars = ['(',')', ',','\'']
"""
# input comes from STDIN
for line in sys.stdin:
    line = line.strip()
    for ctch in bad_chars:
        line = line.replace(ctch,'')
    line = line.strip()
    line = line.lower()
    word_n_count = line.split()
    count = int(word_n_count[1])
    if word_n_count[0] in word_map.keys():
        word_map[word_n_count[0]] += count
    else:
        word_map[word_n_count[0]] = count

for wrd in word_map.keys():
    print(wrd, word_map[wrd])
"""

import sys

mut_map = {'Silent' : [],'Missense' : [] , 'Nonsense' : []}
transition = []
transversion = []
#print('Edit Mutations: \n')
#print('pos\torig\treplace')
transit_fd = open("Transitions.txt",'w')
transverse_fd = open("Transversions.txt",'w')
mutations_fd = open("Mutations.txt",'w')

for line in sys.stdin:
    line = line.strip()
    #for ctch in bad_chars:
     #   line = line.replace(ctch,'')
    mut_type, tup = line.split()
    if mut_type == 'Transit' :
        transition.append(tup)
    elif mut_type == 'Transverse':
        transversion.append(tup)
    else:
        mut_map[mut_type].append(tup)
transition.sort()
if len(transition) != 0:
    for i in transition:
        transit_fd.write(i)
        transit_fd.write("\n")
 else:
    transit_fd.write("No transitions found ")
transit_fd.close() 

transversion.sort()
if len(transversion) != 0:
    for i in transversion:
        transverse_fd.write(i)
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
        mutations_fd.write(tup)
        mutations_fd.write("\n")
mutations_fd.close()
        
    


        
    

    
