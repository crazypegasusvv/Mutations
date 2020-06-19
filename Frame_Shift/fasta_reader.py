def convert_fasta_to_string(fasta_file):
    """
    Function converting file in FASTA format (fasta_file) to string
    """
    
    with open(fasta_file, "r") as f:
        lines = f.readlines()
    return "".join([line.replace("\n", "") for line in lines[1:]])
