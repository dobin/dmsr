import logging
import yaml
from pathlib import Path
import os

from client.network import Network


class Plugin():
    def __init__(self, refresh: int):
        self.name = self.__class__.__name__
        self.refresh = refresh
        self.config = {}


    def run(self):
        pass


    def loadConfig(self):
        filepath = os.path.join('plugins', self.__class__.__name__ + '.yaml')
        p = Path(filepath)
        if not p.is_file():
            # dont care
            return None

        with open(filepath) as f:
            yamlData = yaml.safe_load(f)
            self.config = yamlData
            if 'refresh' in yamlData:
                self.refresh = yamlData['refresh']
            print("  {}".format(yamlData))


    def send(self, data):
        try:
            Network.send(data, self.name, self.refresh)
        except:
            logging.info("Could not reach server, ignoring")
