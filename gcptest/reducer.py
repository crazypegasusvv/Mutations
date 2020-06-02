#!/usr/bin/python
import sys

mut_map = {'Silent' : [],'Missense' : [] , 'Nonsense' : []}
transition = []
transversion = []


def main(argv):
    line = sys.stdin.readline()
    try:
        while line:
            line = line.rstrip()
            splits = line.split("\t", 1)
            mut_type = splits[0].rstrip()
            spits = splits[1].strip()
            spits = spits.split("\t")
            spits[0] = int(spits[0])
            tup = tuple(spits)
            if mut_type == 'Transit':
                transition.append(tup)
            elif mut_type == 'Transverse':
                transversion.append(tup)
            else:
                mut_map[mut_type].append(tup)
            line = sys.stdin.readline()
    except "end of file":
        return None

    transition.sort()
    if len(transition) != 0:
    	print '\nTransitions: \n'
        for i in transition:
            print '%s\t%s\t%s' % (str(i[0]), i[1], i[2])
    else:
        print "No transitions found!"

    transversion.sort()
    if len(transversion) != 0:
    	print '\nTransversions: \n'
        for i in transversion:
        	print '%s\t%s\t%s' % (str(i[0]), i[1], i[2])
    else:
        print "No transitions found"

    for i in mut_map:
        mut_map[i].sort()

    for i,j in mut_map.items():
        print i + ": \n"
        for tup in j:
        	print '%s\t%s\t%s' % (str(tup[0]), tup[1], tup[2])


if __name__ == "__main__":
    main(sys.argv)