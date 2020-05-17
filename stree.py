"""
construct suffix tree separately for coding and non coding regions
"""
from time import perf_counter_ns
import sys


class Node(object):
    """
    A node in the suffix tree.

    suffix_node
        the index of a node with a matching suffix, representing a suffix link.
        -1 indicates this node has no suffix link.
    """

    def __init__(self):
        self.suffix_node = -1

    def __repr__(self):
        return "Node(suffix link: %d)" % self.suffix_node


class Edge(object):
    """
    An edge in the suffix tree.

    first_char_index
        index of start of string part represented by this edge

    last_char_index
        index of end of string part represented by this edge

    source_node_index
        index of source node of edge

    dest_node_index
        index of destination node of edge
    """

    def __init__(self, first_char_index, last_char_index, source_node_index, dest_node_index):
        self.first_char_index = first_char_index
        self.last_char_index = last_char_index
        self.source_node_index = source_node_index
        self.dest_node_index = dest_node_index

    @property
    def length(self):
        return self.last_char_index - self.first_char_index

    def __repr__(self):
        return 'Edge(%d, %d, %d, %d)' % (self.source_node_index, self.dest_node_index,
                                         self.first_char_index, self.last_char_index)


class Suffix(object):
    """Represents a suffix from first_char_index to last_char_index.

    source_node_index
        index of node where this suffix starts

    first_char_index
        index of start of suffix in string

    last_char_index
        index of end of suffix in string
    """

    def __init__(self, source_node_index, first_char_index, last_char_index):
        self.source_node_index = source_node_index
        self.first_char_index = first_char_index
        self.last_char_index = last_char_index

    @property
    def length(self):
        return self.last_char_index - self.first_char_index

    def explicit(self):
        """A suffix is explicit if it ends on a node. first_char_index
        is set greater than last_char_index to indicate this.
        """
        return self.first_char_index > self.last_char_index

    def implicit(self):
        return self.last_char_index >= self.first_char_index


class SuffixTree(object):
    """A suffix tree for string matching. Uses Ukkonen's algorithm
    for construction.
    """

    def __init__(self, string, case_insensitive=False):
        """
        string
            the string for which to construct a suffix tree
        """
        self.string = string
        self.case_insensitive = case_insensitive
        self.N = len(string) - 1
        self.nodes = [Node()]
        self.edges = {}
        self.active = Suffix(0, 0, -1)
        if self.case_insensitive:
            self.string = self.string.lower()
        for chs in range(len(string)):
            self._add_prefix(chs)

    def __repr__(self):
        """
        Lists edges in the suffix tree
        """
        curr_index = self.N
        s = "\tStart \tEnd \tSuf \tFirst \tLast \tString\n"
        values = list(self.edges.values())
        values.sort(key=lambda x: x.source_node_index)
        for edge in values:
            if edge.source_node_index == -1:
                continue
            s += "\t%s \t%s \t%s \t%s \t%s \t" % (edge.source_node_index, edge.dest_node_index,
                                                  self.nodes[edge.dest_node_index].suffix_node,
                                                  edge.first_char_index, edge.last_char_index)

            top = min(curr_index, edge.last_char_index)
            s += self.string[edge.first_char_index:top + 1] + "\n"
        return s

    def _add_prefix(self, last_char_index):
        """
        The core construction method.
        """
        last_parent_node = -1
        while True:
            parent_node = self.active.source_node_index
            if self.active.explicit():
                if (self.active.source_node_index, self.string[last_char_index]) in self.edges:
                    # prefix is already in tree
                    break
            else:
                e = self.edges[self.active.source_node_index, self.string[self.active.first_char_index]]
                if self.string[e.first_char_index + self.active.length + 1] == self.string[last_char_index]:
                    # prefix is already in tree
                    break
                parent_node = self._split_edge(e, self.active)

            self.nodes.append(Node())
            e = Edge(last_char_index, self.N, parent_node, len(self.nodes) - 1)
            self._insert_edge(e)

            if last_parent_node > 0:
                self.nodes[last_parent_node].suffix_node = parent_node
            last_parent_node = parent_node

            if self.active.source_node_index == 0:
                self.active.first_char_index += 1
            else:
                self.active.source_node_index = self.nodes[self.active.source_node_index].suffix_node
            self._canonize_suffix(self.active)
        if last_parent_node > 0:
            self.nodes[last_parent_node].suffix_node = parent_node
        self.active.last_char_index += 1
        self._canonize_suffix(self.active)

    def _insert_edge(self, edge):
        self.edges[(edge.source_node_index, self.string[edge.first_char_index])] = edge

    def _remove_edge(self, edge):
        self.edges.pop((edge.source_node_index, self.string[edge.first_char_index]))

    def _split_edge(self, edge, suffix):
        self.nodes.append(Node())
        e = Edge(edge.first_char_index, edge.first_char_index + suffix.length, suffix.source_node_index,
                 len(self.nodes) - 1)
        self._remove_edge(edge)
        self._insert_edge(e)
        self.nodes[e.dest_node_index].suffix_node = suffix.source_node_index  # need to add node for each edge
        edge.first_char_index += suffix.length + 1
        edge.source_node_index = e.dest_node_index
        self._insert_edge(edge)
        return e.dest_node_index

    def _canonize_suffix(self, suffix):
        """
        This canonizes the suffix, walking along its suffix string until it
        is explicit or there are no more matched nodes.
        """
        if not suffix.explicit():
            e = self.edges[suffix.source_node_index, self.string[suffix.first_char_index]]
            if e.length <= suffix.length:
                suffix.first_char_index += e.length + 1
                suffix.source_node_index = e.dest_node_index
                self._canonize_suffix(suffix)

    # Public methods
    def find_substring(self, substring):
        """Returns the index of substring in string or -1 if it
        is not found.
        """
        if not substring:
            return -1
        if self.case_insensitive:
            substring = substring.lower()
        curr_node = 0
        posi = 0
        """
        tuple (no of charcters matched, status , starting index in the reference string)
                        status = -1 :: There is no edge further
                        status = -2 :: Completely matched string
                        status = n(>=0) :: No of characters matched = no of characters matched + status 
        """
        prev_edge = None
        edge = None
        ln = 0
        while posi < len(substring):
            edge = self.edges.get((curr_node, substring[posi]))  # edge with the starting character substring[posi]
            if not edge:
                if posi > 0:  # posi : no of characters matched so far
                    return posi, -1, prev_edge.first_char_index - posi + ln
                else:
                    return -1, -1, prev_edge
            ln = min(edge.length + 1,
                     len(substring) - posi)  # if string to be found is less than the length of string contained in edge
            if substring[posi:posi + ln] != self.string[edge.first_char_index:edge.first_char_index + ln]:  # mismatch
                # find the extent to which there is a match
                for jn in range(ln):
                    if substring[posi + jn] != self.string[edge.first_char_index + jn]:
                        return posi, jn, edge.first_char_index - posi
                        # print(substring[posi+jn] ," :: ",self.string[edge.first_char_index+jn]," matched ",jn)
                    # else: return (posi,jn,edge.first_char_index - posi) print("In find_substring : ",self.string[
                    # edge.first_char_index:edge.first_char_index+jn]," :: ",substring[posi:posi+jn]," :: ",substring)

                # return -1
            posi += edge.length + 1
            prev_edge = edge
            curr_node = edge.dest_node_index
            # print("In find_substring method :",self.string[edge.first_char_index:edge.first_char_index + ln],
            # " :: ",substring)
        return len(substring), -2, edge.first_char_index - len(substring) + ln

    def has_substring(self, substring):
        return self.find_substring(substring) != -1


"""
test_seq = ['AATGCATGCA$','ATGCATGCAC$']
tree_list = [SuffixTree(x) for x in test_seq]
"""
start_time = perf_counter_ns()
# sys.stdout = open("oput.txt",'w')
#############################################
""" 
instead of writing the coding regions into a file.. make a list of coding and  non coding regions.
    Code_dict : dictionary of coding regions
    Non_Code_dict: dictionary of non coding regions
    key: starting index of region
    value: region
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
#   print(i,":",j)
# print(len(SGC))
print("\t1. Eukaryotes\n\t2. Prokaryotes\n\t3. Motochondrial Genome")
species_type = input("Enter the species index:")
# species type received
s_codon = Start_Codon[int(species_type)]
# start codon found
read_fd = open('ref_seq.txt', 'r')

index = -3

ncflag = 0
scflag = 0
stflag = 0
"""
#codon = read_fd.read(3)

#for i in s_codon:
#	if codon == i:
#		coding_reg_flag = 1
#		fd = coding_fd
#		break

#if coding_reg_flag != 1:
#	non_coding_reg_flag = 1
#	fd = noncoding_fd			

#fd.write(index)
#fd.write(codon)
#index = index + 3
#stop_flag = 0
"""
sfound = 0
cindex = 0
ncdindex = 0
Code_dict = {}
Non_Code_dict = {}
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
            cindex = index
            Code_dict[cindex] = codon
            scflag = 1  # set the start codon flag
            ncflag = 0  # unset the non coding flag
            stflag = 0  # unset stop codon
            sfound = 0  # unset the sfound
        else:  # start codon not found
        	ncdindex = index
            if ncflag == 0:  # non coding flag also not set
                Non_Code_dict[ncdindex] = codon
                ncflag = 1  # set the non coding flag
            else:  # if nc flag is already set and start codon not found then cont writing
                Non_Code_dict[ncdindex] = Non_Code_dict[ncdindex] + codon
    else:  # start codon is already found
        # search if the codon is stop codon or not
        for i in Stop_codon:
            if i == codon:
                stflag = 1  # set the stop codon flag
                break
        if stflag == 1:  # stop codon found
            scflag = 0  # unset the start codon flag
            ncflag = 0  # unset the non coding flag
            Code_dict[cindex] = Code_dict[cindex] + codon
        else:
            Code_dict[cindex] = Code_dict[cindex] + codon
read_fd.close()
sys.stdout = open("oput.txt", 'w')  # redirecting the standard output to the file
for i, j in Code_dict.items():
    print(i, "::", j, "::", len(j))
print("============= Non Coding regions =============")
for i, j in Non_Code_dict.items():
    print(i, "::", j, "::", len(j))
# Constructin suffix trees for each of the coding regions
coding_regions_tree = [SuffixTree(Code_dict[x]) for x in Code_dict]
const_time = perf_counter_ns()
# Printing the suffix trees constructed for coding regions
count = 0
counter = []
for i in Code_dict:
    counter.append(i)
for i in coding_regions_tree:
    print("For coding region : ", counter[count], "::", Code_dict[counter[count]])
    print(i.__repr__())
    count = count + 1
print("=================== Time ======================")
print("Time taken for construction: ", (const_time - start_time) / (10 ** 9))
