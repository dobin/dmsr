import psutil
from typing import Tuple, Dict

from client.plugin import Plugin, PluginStatus


class loggedin(Plugin):
    def __init__(self, refresh):
        super().__init__(refresh)


    def run(self) -> Tuple[Dict, PluginStatus]:
        # Reference: https://pypi.org/project/psutil/
        data = {}
        status = PluginStatus.OK

        users = psutil.users()
        for user in users:
            data[user.terminal] = user.name

        return data, status
