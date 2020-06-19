import constants

from needleman_wunsch_algorithm_config import NeedlemanWunschAlgorithmConfig


def validate_input_data(seq1, seq2, config: NeedlemanWunschAlgorithmConfig):
    """
    Function validating input data: sequences and config
    """

    validation_result = validate_config(config)
    if not validation_result[0]:
        return validation_result

    if len(seq1) > config.MAX_SEQ_LENGTH or len(seq2) > config.MAX_SEQ_LENGTH:
        return False, f"Given sequences are too long! Maximum possible length of sequences is {config.MAX_SEQ_LENGTH}"

    return True, ""


def validate_config(config: NeedlemanWunschAlgorithmConfig):
    """
    Function validating Needleman-Wunsch algorithm config
    """

    parameters_names_list = ["SAME", "DIFF", "GAP_PENALTY", "MAX_NUMBER_PATHS", "MAX_SEQ_LENGTH"]

    for param_name in parameters_names_list:
        if not isinstance(config[param_name], int):
            return False, f"Parameter {param_name} is not int!"
            
    for param_name in parameters_names_list[0:3]:
        if config[param_name] == 0:
            return False, f"Parameter {param_name} can not be equal to 0!"

    for param_name in parameters_names_list[3:]:
        if config[param_name] < 1:
            return False, f"Parameter {param_name} can not be less than 1!"

    if config.SAME <= config.DIFF:
        return False, f"Parameter SAME must be greater than parameter DIFF!"

    if config.MAX_SEQ_LENGTH > constants.MAXIMUM_SEQ_LEN:
        return False, f"Value of parameter MAX_SEQ_LENGTH is too big. It should be less than {constants.MAXIMUM_SEQ_LEN}"

    if config.MAX_NUMBER_PATHS > constants.MAXIMUM_NUMBER_PATHS:
        return False, f"Value of parameter MAX_NUMBER_PATHS is too big. It should be less than {constants.MAXIMUM_NUMBER_PATHS}"

    return True, ""
