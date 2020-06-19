1. Run the needleman - wunsch algorithm to find the alignments
	
	python run.py -a d1.txt -b d2.txt -c config.txt -o nw_output.txt

2. Run perf_ssr module to get the tandem repeats in d1.txt (ref sequence)

	perf -i d1.txt -u 2 

	Output will be in d1_perf.tsv
 
 3. Run the readFRMnw_output.py

 	python readFRMnw_output.py

 	Output will be in the Frame_Shift.txt 	
