import psutil

from client.model import Plugin
from utils import prettyNumber


class sysinfo(Plugin):
    def __init__(self, refresh):
        super().__init__(refresh)
        self.config['disks'] = ['/']
        self.config['show load'] = True
        self.config['show memory'] = True


    def run(self):
        # Reference: https://pypi.org/project/psutil/
        data = {}

        if self.config['show load']:
            data['load'] = list(psutil.getloadavg())

        if self.config['show memory']:
            data['memory'] = {
                'total': prettyNumber(psutil.virtual_memory().total, 1024 * 1024),
                'available': prettyNumber(psutil.virtual_memory().available, 1024 * 1024),
                'used': "{}%".format(psutil.virtual_memory().percent)
            }

        for disk in self.config['disks']:
            data[disk] = {
                'total': prettyNumber(psutil.disk_usage(disk).total, 1024 * 1024),
                'free': prettyNumber(psutil.disk_usage(disk).free, 1024 * 1024),
                'used': "{}%".format(psutil.disk_usage(disk).percent)
            }

        self.send(data)
