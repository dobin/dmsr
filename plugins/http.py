import requests
from typing import Tuple, Dict

from client.plugin import Plugin, PluginStatus
from utils import prettyNumber

class http(Plugin):
    def __init__(self, refresh):
        super().__init__(refresh)
        self.config['urls'] = {}


    def run(self) -> Tuple[Dict, PluginStatus]:
        data = {}
        status = PluginStatus.OK

        for name, url in self.config['urls'].items():
            try:
                page = requests.get(url, timeout=1, verify=False)
                data[name] = 'Up'
            except:
                data[name] = 'Down'
                status = PluginStatus.WARN

        return data, status
