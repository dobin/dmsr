import psutil

from client.model import Plugin


class process(Plugin):
    def __init__(self, refresh):
        super().__init__(refresh)
        self.config['processes'] = [ ]


    def run(self):
        # Reference: https://pypi.org/project/psutil/
        data = {}

        for process in self.config['processes']:
            data[process] = 'down'

        for proc in psutil.process_iter(['pid', 'name']):
            for process in self.config['processes']:
                if proc.info['name'] == process:
                    data[process] = 'up'

        self.send(data)
