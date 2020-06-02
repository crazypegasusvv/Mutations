#!/usr/bin/python
import sys

mut_map = {'Silent' : [],'Missense' : [] , 'Nonsense' : []}
transition = []
transversion = []
transit_fd = open("Transitions.txt",'w')
transverse_fd = open("Transversions.txt",'w')
mutations_fd = open("Mutations.txt",'w')


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


if __name__ == "__main__":
    main(sys.argv)