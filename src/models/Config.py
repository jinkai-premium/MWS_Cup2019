# coding: utf-8
from pathlib import Path
from yaml import load, BaseLoader


class Config(object):
    def __init__(self):
        self.root_directory = Path(__file__).parent.parent.parent
        self.config_file = self.root_directory / Path('src/configs/config.yaml')
        self.load_settings()

    def load_settings(self):
        for key, value in load(self.config_file.read_text(), Loader=BaseLoader).items():
            setattr(self, key, value)
