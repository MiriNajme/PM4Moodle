from configparser import ConfigParser


class ConfigService:
    def __init__(self, config_file="../config.cfg"):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        parser = ConfigParser()
        parser.read(self.config_file)
        return parser

    def get_config(self):
        return self.config

    def save_config(self, config=None):
        if config is not None:
            self.config = config
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)
