#!/usr/bin/python
import sys

def main(argv):
	codons = []
	line = sys.stdin.readline()
	sflag = 0
#pflag = 0
	try:
		while line:
			line = line.rstrip()
			splits = line.split(':')
			codon_type = int(splits[0])
			index = int(splits[1])
			codons.append((index,codon_type))

			line = sys.stdin.readline()
	except "end of file":
		return None		

	codons.sort()
	strt_codon = []
	stp_codon = []
	for i in range(len(codons)):
		tup = codons[i]
		codon_type = tup[1]
		index = tup[0]
		if codon_type == 1 and sflag == 0:
			strt_codon.append(index)
			sflag = 1

		if codon_type == 2 and sflag == 1:
			stp_codon.append(index)
			sflag = 0	

	print(len(strt_codon)," : ",len(stp_codon))
	#sys.stdout = open("reg.txt",'w')
	fd = open("ref_pyth.txt",'r')
	for i in range(len(strt_codon)):
		strt_indx = strt_codon[i]
		stp_indx = stp_codon[i]
		fd.seek(strt_indx,0)
		reg = fd.read(stp_indx - strt_indx + 3)
		print(strt_indx," : ",reg)

if __name__ == '__main__':
	main(sys.argv)		



