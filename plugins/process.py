import psutil
from typing import Tuple, Dict

from client.plugin import Plugin, PluginStatus


class process(Plugin):
    def __init__(self, refresh):
        super().__init__(refresh)
        self.config['processes'] = [ ]


    def run(self) -> Tuple[Dict, PluginStatus]:
        # Reference: https://pypi.org/project/psutil/
        data = {}
        status = PluginStatus.OK

        for process in self.config['processes']:
            data[process] = 'down'

        for proc in psutil.process_iter(['pid', 'name']):
            for process in self.config['processes']:
                if proc.info['name'] == process:
                    data[process] = 'Up'

        for process in data:
            if data[process] != 'Up':
                status = PluginStatus.WARN
                break

        return data, status
