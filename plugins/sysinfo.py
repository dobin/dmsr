import psutil
from typing import Tuple, Dict

from client.plugin import Plugin, PluginStatus
from utils import prettyNumber


class sysinfo(Plugin):
    def __init__(self, refresh):
        super().__init__(refresh)
        self.config['disks'] = ['/']
        self.config['show load'] = True
        self.config['show memory'] = True
        self.config['danger percent'] = 90


    def run(self) -> Tuple[Dict, PluginStatus]:
        # Reference: https://pypi.org/project/psutil/
        data = {}
        status = PluginStatus.OK

        if self.config['show load']:
            data['load'] = [
                round(psutil.getloadavg()[0], 2),
                round(psutil.getloadavg()[1], 2),
                round(psutil.getloadavg()[2], 2)
            ]
            if psutil.getloadavg()[2] > self.config['danger percent']:
                status = PluginStatus.INFO

        if self.config['show memory']:
            data['memory'] = {
                'total': prettyNumber(psutil.virtual_memory().total, 1024 * 1024),
                'available': prettyNumber(psutil.virtual_memory().available, 1024 * 1024),
                'used': "{}%".format(psutil.virtual_memory().percent)
            }
            if psutil.virtual_memory().percent > self.config['danger percent']:
                status = PluginStatus.INFO

        for disk in self.config['disks']:
            data[disk] = {
                'total': prettyNumber(psutil.disk_usage(disk).total, 1024 * 1024),
                'free': prettyNumber(psutil.disk_usage(disk).free, 1024 * 1024),
                'used': "{}%".format(psutil.disk_usage(disk).percent)
            }
            if psutil.disk_usage(disk).percent > self.config['danger percent']:
                status = PluginStatus.INFO

        return data, status
