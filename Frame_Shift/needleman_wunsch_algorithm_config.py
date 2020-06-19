from config import Config


class NeedlemanWunschAlgorithmConfig(Config):
    """
    Class representing Needleman-Wunsch algorithm config
    """

    def __init__(self, config_file = "config.txt", manual = False):
        if manual:
            self.SAME = 0
            self.DIFF = 0
            self.GAP_PENALTY = 0
            self.MAX_NUMBER_PATHS = 0
            self.MAX_SEQ_LENGTH = 0
            return

        Config.__init__(self, config_file)
        try:
            self.SAME = self["SAME"]
            self.DIFF = self["DIFF"]
            self.GAP_PENALTY = self["GAP_PENALTY"]
            self.MAX_NUMBER_PATHS = self["MAX_NUMBER_PATHS"]
            self.MAX_SEQ_LENGTH = self["MAX_SEQ_LENGTH"]
        except KeyError as ke:
            raise Exception(f"Key {ke} is missing in config file")
            