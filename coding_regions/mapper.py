#!/usr/bin/python

import sys

Start_Codon = {1: ['ATG'], 2: ['GTG', 'TTG'], 3: ['ATA', 'ATT']}
Stop_codon = ['TAA', 'TAG', 'TGA']
SC = []
stc = []
#sys.stdout = open("cregions.txt",'w')
def find_codons(sindex, line, s_codon):
	#print("====================for===============",sindex,"\n")
	i = 0
	sflag = 0
	pflag = 0
	while i<len(line):
		codon = line[i : i + 3]
		if sflag == 0:
			for c in s_codon:
				if c == codon:
					sflag = 1
					pflag = 0
					SC.append(sindex + i)
					print("1:",sindex+i)
					break
		if pflag == 0:
			for c in Stop_codon:
				if c ==  codon:
					pflag = 1
					sflag = 0
					stc.append(sindex + i)
					print("2:",sindex + i)
					break			
		i = i + 3						

def main(argv):
	sp_type = 1
	line = sys.stdin.read(75)
	s_codon = Start_Codon[sp_type]
	sindex = 0
	try:
		while line:
			line = line.rstrip()
			find_codons(sindex, line, s_codon)
			sindex = sindex + 75
			line = sys.stdin.read(75)
	except "end of file":
		return None

if __name__ == "__main__":
	main(sys.argv)


