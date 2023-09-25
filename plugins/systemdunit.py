import os
from typing import Tuple, Dict

from client.plugin import Plugin


class systemdunit(Plugin):
    def __init__(self, refresh):
        super().__init__(refresh)
        self.config['processes'] = [ ]


    def run(self) -> Tuple[Dict, str]:
        data = {}
        status = ''

        for unit in self.config['units']:
            sh = 'service {} status >/dev/null 2>&1'.format(unit)
            stat = os.system(sh)

            if stat == 0:
                data[unit] = 'up'
            else:
                # get error
                data[unit] = "error: {}".format(stat)


        return data, status
