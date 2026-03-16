import yaml

class ProgramConfig:

    def __init__(self, config_dict):

        self.data = config_dict

    def get(self, category, parameter):

        return self.data[category][parameter]

    def set(self, category, parameter, value):

        self.data[category][parameter] = value


def load_config(path="config/defaults.yaml"):

    with open(path, "r") as f:
        config_dict = yaml.safe_load(f)

    return ProgramConfig(config_dict)