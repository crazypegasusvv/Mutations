#!/usr/bin/python
import os
import sys
from subprocess import PIPE, Popen
from pandas import DataFrame

mut_map = {
	'Silent' : [],
	'Missense' : [],
	'Nonsense' : []
}
transition = []
transversion = []

transverses = "Transverses.csv"
transitions = "Transitions.csv"

outdir = 'muts'
username = 'virinchi'
tran_path = os.path.join(os.sep, outdir, transitions)
trans_path = os.path.join(os.sep, outdir, transverses)

mut_files = ["Silents.csv", "Missenses.csv", "Nonsenses.csv"]
mut_paths = [os.path.join(os.sep, outdir, type_name) for type_name in mut_files]

def main(argv):
    line = sys.stdin.readline()
    try:
        while line:
            line = line.rstrip()
            splits = line.split("\t", 1)
            type_change = splits[0].rstrip()
            spits = splits[1].strip()
            spits = spits.split("\t")
            spits[0] = int(spits[0])
            tup = tuple(spits)
            if type_change == 'Transit':
                transition.append(tup)
            elif type_change == 'Transverse':
                transversion.append(tup)
            else:
                mut_map[type_change].append(tup)
            line = sys.stdin.readline()
    except "end of file":
        return None
    
    if len(transition):
        transition.sort()
        trandf = DataFrame(transition, columns = ['index', 'nucleotide', 'transition'])
        trandf.set_index('index', inplace=True)
        trandf.to_csv(transitions)
        put = Popen(["hdfs", "dfs", "-put", transitions, tran_path], stdin=PIPE, bufsize=-1)
        put.communicate()

    if len(transversion):
        transversion.sort()
        transdf = DataFrame(transversion, columns = ['index', 'nucleotide', 'transversion'])
        transdf.set_index('index', inplace=True)
        transdf.to_csv(transverses)
        put = Popen(["hdfs", "dfs", "-put", transverses, trans_path], stdin=PIPE, bufsize=-1)
        put.communicate()
    
    for mut_type in mut_map:
        if len(mut_map[mut_type]):
            mut_map[mut_type].sort()
            typedf = DataFrame(mut_map[mut_type], columns=['index', 'sequence', mut_type + '_mutation'])
            typedf.set_index('index', inplace=True)
            type_index = list(mut_map.keys()).index(mut_type)
            typedf.to_csv(mut_files[type_index])
            put = Popen(["hdfs", "dfs", "-put", mut_files[type_index], mut_paths[type_index]], stdin=PIPE, bufsize=-1)
            put.communicate()


if __name__ == "__main__":
    main(sys.argv)
