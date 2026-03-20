import yaml

class ProgramConfig:

    def __init__(self, config_dict):
        self.data = config_dict

    def get(self, *keys, default=None):
        """
        Access nested config values with unlimited depth.
        Example: get("materials", "composite_material", "price_per_kg")
        """
        value = self.data
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, *keys, value):
        """
        Set nested config value.
        Example: set("materials", "composite_material", "price_per_kg", value=200)
        """
        d = self.data
        for key in keys[:-1]:
            d = d.setdefault(key, {})
        d[keys[-1]] = value


def load_config(path="config/defaults.yaml"):
    with open(path, "r") as f:
        config_dict = yaml.safe_load(f)

    return ProgramConfig(config_dict)