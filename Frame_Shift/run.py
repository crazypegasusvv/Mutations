import fasta_reader as fr
import input_data_validator as idv
import sys
import getopt
from datetime import datetime

from needleman_wunsch_algorithm_config import NeedlemanWunschAlgorithmConfig
from needleman_wunsch_algorithm import NeedlemanWunschAlgorithm


if __name__ == "__main__":
    # Set the recursion limit i.e over writing the defualt value of 1000 recursion limit
    sys.setrecursionlimit(10000)

    # Get the arguments from the command-line except the filename
    argv = sys.argv[1:]

    try:
        startTime = datetime.now()
        # Define the getopt parameters
        opts, args = getopt.getopt(argv, "a:b:c:o:", ["sequence1", "sequence2", "config", "output"])

        # Check if the options' length is 4
        if len(opts) != 4:
            print("Wrong options and parameters! \nUsage: add.py -a <sequence1> -b <sequence2> -c <config> -o <output> \nwhere sequence1, sequence2, config, output are txt files.")
        else:
            # Create dictionary of input arguments
            inputs = {}
            for opt, arg in opts:
                opt = opt.replace("-", "")
                inputs[opt] = arg

            # Create input variables for algorithm
            fasta_file1 = inputs["a"]
            fasta_file2 = inputs["b"]
            configuration_file = inputs["c"]
            output_file = inputs["o"]
            
            # Load sequences from files to strings
            sequence1 = fr.convert_fasta_to_string(fasta_file1)
            sequence2 = fr.convert_fasta_to_string(fasta_file2)
            
            # Load configuration file and create config object with configuration data
            config = NeedlemanWunschAlgorithmConfig(configuration_file)
            
            # Check if input data are valid
            validation_result = idv.validate_input_data(sequence1, sequence2, config)
            
            # If input data are correct then run algorithm
            if validation_result[0]:
                nwa = NeedlemanWunschAlgorithm(sequence1, sequence2, config)
                nwa.print_results(output_file)
            else:
                print(validation_result[1])
            endTime = datetime.now()
            print("Time taken: ",endTime - startTime)        

    except getopt.GetoptError:
        print("Wrong options and parameters! \nUsage: add.py -a <sequence1> -b <sequence2> -c <config> -o <output> \nwhere sequence1, sequence2, config, output are txt files.")
        sys.exit(2)