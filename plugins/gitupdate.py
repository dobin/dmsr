from typing import Tuple, Dict
import os
import subprocess
import logging

from client.plugin import Plugin


class gitupdate(Plugin):
    def __init__(self, refresh):
        super().__init__(refresh)
        self.config['paths'] = [  ]


    def run(self) -> Tuple[Dict, str]:
        data = {}
        status = ''

        for path in self.config['paths']:
            if not os.path.exists(path):
                logging.error('Plugin gitupdate: {} does not exist'.format(path))
                data[path] = "Not exist"
                continue

            cmd = 'cd {}; git log --date=short -n1'.format(path)
            output = subprocess.check_output(cmd, shell=True).decode('utf-8')
            # example output: 
            # Author: Dobin <dobin@broken.ch>
            # Date:   Wed Apr 5 18:23:38 2023 +0200
            #
            #     fix: ignore missing config entry for plugin
            lines = output.splitlines()
            for line in lines:
                if line.startswith('Date:'):
                    dir = os.path.basename(path)
                    data[dir] = line.split('   ')[1]

        return data, status
