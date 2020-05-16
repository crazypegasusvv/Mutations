"""
identifying coding and non-coding(junk) regions of DNA using Start Codon and Stop Codon
Start codon to Stop codon : Coding Region
Stop codon to the next Star Codon: Non-coding Region

We will use DNA Standard Genetic Code to identify these regions.
Depending upon the type of organisms these codons vary.
We will maintain DNA - SGC as a dictionary named SGC
index: codon
value: amino acid
easy to access

We shall maintain a dictionary Start_Codon, of Start codons for each types of organism so that
this code can be used for finding mutations in all types of genomes.
index: species name
value: start codon
The most common start codon is ATG
1.candida albicans in eukaryotes uses CAG, Mammalian cells can initiate translation with CTG
2.Prokaryotes uses GTG,TTG mostly
3.Mitochondrial genome : ATA , ATT
"""

Start_Codon = {1: ['ATG', 'CTG', 'CAG'], 2: ['GTG', 'TTG'], 3: ['ATA', 'ATT']}
Stop_codon = ['TAA', 'TAG', 'TGA']
SGC = {'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L', 'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L', 'ATT': 'I',
       'ATC': 'I', 'ATA': 'I', 'ATG': 'M', 'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V', 'TCT': 'S', 'TCC': 'S',
       'TCA': 'S', 'TCG': 'S', 'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P', 'ACT': 'T', 'ACC': 'T', 'ACA': 'T',
       'ACG': 'T', 'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A', 'TAT': 'Y', 'TAC': 'Y', 'TAA': 'Stop', 'TAG': 'Stop',
       'TGA': 'Stop', 'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q', 'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
       'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E', 'TGT': 'C', 'TGC': 'C', 'TGG': 'W', 'CGT': 'R', 'CGC': 'R',
       'CGA': 'R', 'CGG': 'R', 'AGA': 'R', 'AGG': 'R', 'AGT': 'S', 'AGC': 'S', 'GGT': 'G', 'GGC': 'G', 'GGA': 'G',
       'GGG': 'G'}

# for i,j in SGC.items():
# print(i,":",j)
# print(len(SGC))

print("\t1. Eukaryotes\n\t2. Prokaryotes\n\t3. Motochondrial Genome")
species_type = input("Enter the species index:")
# species type received
s_codon = Start_Codon[int(species_type)]
# start codon found
coding_fd = open("coding_region.txt", 'w')
noncoding_fd = open("non_coding_region.txt", 'w')
read_fd = open('re.txt', 'r')

index = -3

ncflag = 0
scflag = 0
stflag = 0

"""
codon = read_fd.read(3)

#for i in s_codon:
#	if codon == i:
#		coding_reg_flag = 1
#		fd = coding_fd
#		break

#if coding_reg_flag != 1:
#	non_coding_reg_flag = 1
#	fd = noncoding_fd			

fd.write(index)
fd.write(codon)
index = index + 3
stop_flag = 0
"""

sfound = 0
while 1:
    codon = read_fd.read(3)
    index = index + 3
    if not codon:
        break

    if scflag == 0:
        # search for the start codon
        for i in s_codon:
            if i == codon:  # start codon found
                sfound = 1
                break
        if sfound == 1:  # start codon found
            noncoding_fd.write("\n")
            coding_fd.write(str(index))
            coding_fd.write(":")
            coding_fd.write(codon)
            coding_fd.write(" ")
            scflag = 1  # set the start codon flag
            ncflag = 0  # unset the non coding flag
            stflag = 0  # unset stop codon
            sfound = 0  # unset the sfound
        else:  # start codon not found
            if ncflag == 0:  # non coding flag also not set
                coding_fd.write("\n")
                noncoding_fd.write(str(index))
                noncoding_fd.write(":")
                noncoding_fd.write(codon)
                noncoding_fd.write(" ")
                ncflag = 1  # set the non coding flag
            else:  # if nc flag is already set and start codon not found then cont writing
                noncoding_fd.write(codon)
                noncoding_fd.write(" ")
    else:  # start codon is already found
        # search if the codon is stop codon or not
        for i in Stop_codon:
            if i == codon:
                stflag = 1  # set the stop codon flag
                break
        if stflag == 1:  # stop codon found
            scflag = 0  # unset the start codon flag
            ncflag = 0  # unset the non coding flag
            coding_fd.write(codon)
            coding_fd.write(" ")
        else:
            coding_fd.write(codon)
            coding_fd.write(" ")
