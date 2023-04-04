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


    def setConfig(self, config):
        self.config = config


    def send(self, data):
        try:
            Network.send(data, self.name, self.refresh)
        except:
            logging.info("Could not reach server, ignoring")
