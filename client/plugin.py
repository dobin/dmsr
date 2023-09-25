from typing import Tuple, Dict
from enum import Enum


class PluginStatus(Enum):
    OK = ""
    WARN = "warn"
    INFO = "info"
    ERROR = "error"


class Plugin():
    def __init__(self, refresh: int):
        self.name = self.__class__.__name__
        self.refresh = refresh
        self.private = False
        self.config = {}


    def run(self) -> Tuple[Dict, PluginStatus]:
        pass


    def setConfig(self, config):
        # copy new configs
        # leave initial config alone (if config value doesnt exist)
        for key in config:
            self.config[key] = config[key]

        # general configs not specific to a plugin
        if 'refresh' in config:
            self.refresh = config['refresh'] 
        if 'private' in config:
            self.private = config['private'] 
