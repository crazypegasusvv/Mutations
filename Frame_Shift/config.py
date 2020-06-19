import try_parse as tp


class Config:
    """
    Class representing configuration
    """

    def __init__(self, config_file = "config.txt"):
        self.config_file = config_file
        self.config_dict = self._load_config(self.config_file)


    def _load_config(self, configuration_file):
        config = {}
        with open(configuration_file, "r") as conf_file:
            for line in conf_file:
                name, val = line.partition("=")[::2]
                config[name.strip()] = tp.to_int(val.replace("\n", ""))[0]
        return config


    def __getitem__(self, key):
        return self.config_dict[key]
    