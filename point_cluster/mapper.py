#!/usr/bin/python

import sys

Start_Codon = {1: ['ATG'], 2: ['GTG', 'TTG'], 3: ['ATA', 'ATT']}
Stop_codon = ['TAA', 'TAG', 'TGA']
SGC = {'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L', 'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L', 'ATT': 'I',
       'ATC': 'I', 'ATA': 'I', 'ATG': 'M', 'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V', 'TCT': 'S', 'TCC': 'S',
       'TCA': 'S', 'TCG': 'S', 'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P', 'ACT': 'T', 'ACC': 'T', 'ACA': 'T',
       'ACG': 'T', 'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A', 'TAT': 'Y', 'TAC': 'Y', 'TAA': 'Stop', 'TAG': 'Stop',
       'TGA': 'Stop', 'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q', 'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
       'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E', 'TGT': 'C', 'TGC': 'C', 'TGG': 'W', 'CGT': 'R', 'CGC': 'R',
       'CGA': 'R', 'CGG': 'R', 'AGA': 'R', 'AGG': 'R', 'AGT': 'S', 'AGC': 'S', 'GGT': 'G', 'GGC': 'G', 'GGA': 'G',
       'GGG': 'G'}


def is_stopCodon(codon):
    for i in Stop_codon:
        if codon == i:
            return True
    return False


def detect_mutations(strt_indx, ref_seq, test_seq):
    Transition = []
    Transversion = []
    Mutations = {'Silent': [], 'Missense': [], 'Nonsense': []}
    Code_dict = {}
    Code_dict[strt_indx] = ref_seq
    for strt_indx, ref_seq in Code_dict.items():
        index = 0
        i = 0
        while i < len(test_seq):
            m_s_found = 0
            if test_seq[i] != ref_seq[i]:
                pos = i % 3
                index = i
                if pos == 0:
                    ref_codon = ref_seq[index: index + 3]
                    m_codon = test_seq[index: index + 3]
                    i = i + 3
                elif pos == 1:
                    ref_codon = ref_seq[index - 1: index + 2]
                    m_codon = test_seq[index - 1: index + 2]
                    i = i + 2
                else:
                    ref_codon = ref_seq[index - 2: index + 1]
                    m_codon = test_seq[index - 2: index + 1]
                    i = i + 1
                m_s_found = 1
            else:
                i = i + 1

            if m_s_found == 1:
                for ind in range(len(m_codon)):
                    if (m_codon[ind] == 'A' and ref_codon[ind] == 'G') or (
                            m_codon[ind] == 'G' and ref_codon[ind] == 'A'):
                        Transition.append((strt_indx + index + ind, ref_codon[ind], m_codon[ind]))
                    elif (m_codon[ind] == 'T' and ref_codon[ind] == 'C') or (
                            m_codon[ind] == 'C' and ref_codon[ind] == 'T'):
                        Transition.append((strt_indx + index + ind, ref_codon[ind], m_codon[ind]))
                    elif m_codon[ind] != ref_codon[ind]:
                        Transversion.append((strt_indx + index + ind, ref_codon[ind], m_codon[ind]))
                if SGC[ref_codon] == SGC[m_codon]:
                    Mutations['Silent'].append((strt_indx + index + ind, ref_codon, m_codon))
                elif is_stopCodon(m_codon) and not is_stopCodon(ref_codon):
                    Mutations['Nonsense'].append((strt_indx + index + ind, ref_codon, m_codon))
                    break
                else:
                    Mutations['Missense'].append((strt_indx + index + ind, ref_codon, m_codon))

    for i in Transition:
        print 'Transit\t%s\t%s\t%s' % (str(i[0]), i[1], i[2])
    for i in Transversion:
        print 'Transverse\t%s\t%s\t%s' % (str(i[0]), i[1], i[2])
    for i in Mutations:
        l = Mutations[i]
        for j in l:
            print '%s\t%s\t%s\t%s' % (i, str(j[0]), j[1], j[2])


Mutations = {'Silent': [], 'Missense': [], 'Nonsense': []}


def main(argv):
    seq_fd = open("genome.seq", 'r')
    line = sys.stdin.readline()
    try:
        while line:
            line = line.rstrip()
            splits = line.split(':')
            coding_region = splits[1].replace(" ", "")
            ref_seq = coding_region
            seq_fd.seek(int(splits[0]), 0)
            test_seq = seq_fd.read(len(coding_region))
            detect_mutations(int(splits[0]), ref_seq, test_seq)
            line = sys.stdin.readline()
    except "end of file":
        return None
    seq_fd.close()


if __name__ == "__main__":
    main(sys.argv)
