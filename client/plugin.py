import logging
import yaml
from pathlib import Path
import os

from client.network import Network


class Plugin():
    def __init__(self, refresh: int):
        self.name = self.__class__.__name__
        self.refresh = refresh
        self.private = False
        self.config = {}


    def run(self):
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
