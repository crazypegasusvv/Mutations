1. To test mapper manually:
	Un comment the commented line sys.stdout..
	python mapper.py <ref_pyth.txt

2. To test reducer manually:
	Un comment the commented line sys.stdout
	python reducer.py <cregions.txt

################################################
mapper.py and reducer.py when run on a cluster will generate coding regions for the file ref_pyth.txt. This file size is 162483 base pairs.
When run, 412 regions are to be identified.	
