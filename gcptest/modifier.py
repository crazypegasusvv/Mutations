
fp = open('seq.fasta', 'r')
ofp = open('test.seq', 'w+')

line = fp.readline()
line = fp.readline()
cur = 0

while line:
	line = line.strip()
	ofp.write(str(cur) + " " + line + "\n")
	cur += len(line)
	line = fp.readline()
