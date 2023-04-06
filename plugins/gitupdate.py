from typing import Tuple
import os
import subprocess
import logging

from client.model import Plugin


class gitupdate(Plugin):
    def __init__(self, refresh):
        super().__init__(refresh)
        self.config['gitrepos'] = [  ]


    def run(self) -> Tuple[str, str]:
        data = {}
        status = ''

        for path in self.config['gitrepos']:
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
            line = output.splitlines()[2]
            data[path] = line.split('   ')[1]

        return data, status
