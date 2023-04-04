import psutil
from typing import Tuple

from client.model import Plugin


class process(Plugin):
    def __init__(self, refresh):
        super().__init__(refresh)
        self.config['processes'] = [ ]


    def run(self) -> Tuple[str, str]:
        # Reference: https://pypi.org/project/psutil/
        data = {}
        status = ''

        for process in self.config['processes']:
            data[process] = 'down'

        for proc in psutil.process_iter(['pid', 'name']):
            for process in self.config['processes']:
                if proc.info['name'] == process:
                    data[process] = 'up'

        for process in data:
            if process != 'up':
                status = 'warn'
                break

        return data, status
