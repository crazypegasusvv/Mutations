#import sys

#sys.stdout = open("oput.txt",'w')
Start_Codon = {1:['ATG'],2:['GTG','TTG'],3:['ATA','ATT']}
Stop_codon = ['TAA','TAG','TGA']
SGC = {'TTT':'F','TTC':'F','TTA':'L','TTG':'L','CTT':'L','CTC':'L','CTA':'L','CTG':'L','ATT':'I','ATC':'I','ATA':'I','ATG':'M','GTT':'V','GTC':'V','GTA':'V','GTG':'V','TCT':'S','TCC':'S','TCA':'S','TCG':'S','CCT':'P','CCC':'P','CCA':'P','CCG':'P','ACT':'T','ACC':'T','ACA':'T','ACG':'T','GCT':'A','GCC':'A','GCA':'A','GCG':'A','TAT':'Y','TAC':'Y','TAA':'Stop','TAG':'Stop','TGA':'Stop','CAT':'H','CAC':'H','CAA':'Q','CAG':'Q','AAT':'N','AAC':'N','AAA':'K','AAG':'K','GAT':'D','GAC':'D','GAA':'E','GAG':'E','TGT':'C','TGC':'C','TGG':'W','CGT':'R','CGC':'R','CGA':'R','CGG':'R','AGA':'R','AGG':'R','AGT':'S','AGC':'S','GGT':'G','GGC':'G','GGA':'G','GGG':'G'}	

def is_stopCodon(codon):
	for i in Stop_codon:
		if codon == i:
			return True
	return False	
def detect_mutations(strt_indx,ref_seq,test_seq):
	#rint("================ Mutations in ",testfile,"===================")
	Transition = []
	Transversion = []
	Mutations = { 'Silent' : [] ,'Missense' : [] ,'Nonsense' : [] }
	#seq_fd = open(testfile,'r')
	Code_dict = {}
	Code_dict[strt_indx] = ref_seq
	for strt_indx,ref_seq in Code_dict.items():
		#seq_fd.seek( strt_indx , 0 ) # put the pointer at the index distance starting from start of the file
		#test_seq = seq_fd.read(len(ref_seq)) # reading only coding region of reference sequence from test seq
		index = 0
		i = 0
		m_region = 0
		while i < len(test_seq):
			m_s_found = 0
			if test_seq[i] != ref_seq[i] : #mutation found
			#get to know which nucleotide of codon got mutated
				pos = i%3
				index = i
				if pos == 0:
					ref_codon = ref_seq[index : index + 3]
					m_codon = test_seq[index : index + 3]
					i = i + 3
				elif pos == 1:
					ref_codon = ref_seq[index - 1 : index + 2]
					m_codon = test_seq[index - 1 : index + 2]	
					i = i + 2
				else:
					ref_codon = ref_seq[index - 2 : index + 1]
					m_codon = test_seq[index - 2 : index + 1]
					i = i + 1
				m_s_found = 1	
				m_region = 1 #mutation found in this region	

			else:#no mutation found..cont finding the mutation
				i = i + 1	


			if m_s_found == 1: #there is a mutation here
				m_s_found = 0 #in order to find furthur mutations in other codons in this sequence				
			#identifying the type of mutation
			#identifying transition or transversion
				for ind in range(len(m_codon)):
					if (m_codon[ind] == 'A' and ref_codon[ind] == 'G') or (m_codon[ind] == 'G' and ref_codon[ind] == 'A'):
						Transition.append((strt_indx + index + ind,ref_codon[ind],m_codon[ind]))
					elif (m_codon[ind] == 'T' and ref_codon[ind] == 'C') or (m_codon[ind] == 'C' and ref_codon[ind] == 'T'):
			#print("Transition from ",ref_codon[ind]," to ",m_codon[ind])
						Transition.append((strt_indx + index + ind,ref_codon[ind],m_codon[ind]))
					elif m_codon[ind] != ref_codon[ind]:
			#print("Transversion from ",ref_codon[ind]," to ",m_codon[ind])
						Transversion.append((strt_indx + index + ind,ref_codon[ind],m_codon[ind]))

			#identifying the consequences i.e silent or miss_sense or non_sense
				if SGC[ref_codon] == SGC[m_codon]:
			#print("Silent Mutation ",ref_codon," :: ",m_codon)
					Mutations['Silent'].append((strt_indx + index , ref_codon , m_codon))
				elif is_stopCodon(m_codon) and not is_stopCodon(ref_codon):
				#print("Nonsense mutation ",ref_codon," :: ",m_codon)
					Mutations['Nonsense'].append((strt_indx+index , ref_codon , m_codon))
					break
				else:
			#print("Missense Mutation ",ref_codon," :: ",m_codon)
					Mutations['Missense'].append((strt_indx + index , ref_codon , m_codon))
		if m_region == 0:
			print("No Mutations took place in the coding region : ",strt_indx," :: ",ref_seq)				

	#seq_fd.close()

	#print("============== Transitions ====================")
	for i in Transition:
		print("Transit\t", i )
	#print("=============== Transversions =================")
	for i in Transversion:
		print("Transverse\t",i)
	#print("=============== Mutations =====================")
	for i in Mutations:
		l = Mutations[i]
		for j in l:
			print(i,"\t",j) 

coding_fd_read = open("coding_reg.txt",'r')
#to skip the space i.e first empty line
Mutations = { 'Silent' : [] ,'Missense' : [] ,'Nonsense' : [] }
line = coding_fd_read.readline()
seq_fd = open("10794_KY606272_1.txt",'r')
while 1:
	line = coding_fd_read.readline()
	if not line:
		break
	line = line.strip()
	splits = line.split(':')
	#print("index : ",splits[0])
	#print("coding_reg_space :",splits[1])
	coding_region = splits[1].replace(" ","")
	ref_seq = coding_region
	#print("space_removed : ",coding_region)
	seq_fd.seek( int(splits[0]) , 0 ) # put the pointer at the index distance starting from start of the file
	test_seq = seq_fd.read(len(coding_region)) # reading only coding region of reference sequence from test seq
	#print("Test sequence: ",test_seq)
	#print(int(splits[0]))
	detect_mutations(int(splits[0]),ref_seq,test_seq)
coding_fd_read.close()	
seq_fd.close()
#for i,j in Mutations.items():
#	print(i," : ",j)
