import requests
from typing import Tuple, Dict

from client.plugin import Plugin
from utils import prettyNumber


class http(Plugin):
    def __init__(self, refresh):
        super().__init__(refresh)
        self.config['urls'] = []


    def run(self) -> Tuple[Dict, str]:
        data = {}
        status = ""

        for url in self.config['urls']:
            try:
                page = requests.get(url, timeout=1)
                data[url] = 'Up'
            except:
                data[url] = 'Down'
                status = "warn"

        return data, status
