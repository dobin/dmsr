import psutil
from typing import Tuple, Dict

from client.plugin import Plugin


class process(Plugin):
    def __init__(self, refresh):
        super().__init__(refresh)
        self.config['processes'] = [ ]


    def run(self) -> Tuple[Dict, str]:
        # Reference: https://pypi.org/project/psutil/
        data = {}
        status = ''

        for process in self.config['processes']:
            data[process] = 'down'

        for proc in psutil.process_iter(['pid', 'name']):
            for process in self.config['processes']:
                if proc.info['name'] == process:
                    data[process] = 'Up'

        for process in data:
            if data[process] != 'Up':
                status = 'warn'
                break

        return data, status
