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

mut_map = {}

print('Edit Mutations: \n')
print('pos\torig\treplace')

for line in sys.stdin:
    line = line.strip()
    for ctch in bad_chars:
        line = line.replace(ctch,'')
    num, seq = line.split()
    num = int(num)
    if num in mut_map.keys():
        seq0 = mut_map[num]
        for pos in range(len(seq0)):
            if seq[pos] != seq0[pos]:
                epos = num + pos
                print(str(epos) + '\t' + seq0[pos] + '\t' + seq[pos] + '\n')
    else:
        mut_map[num] = seq
