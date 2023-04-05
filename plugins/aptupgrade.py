from typing import Tuple
import os
import subprocess
import logging

from client.model import Plugin


class aptupgrade(Plugin):
    def __init__(self, refresh):
        super().__init__(refresh)


    def run(self) -> Tuple[str, str]:
        data = {}
        status = ''

        if not os.path.exists('/var/log/apt/history.log'):
            status = 'error'
            logging.error('/var/log/apt/history.log does not exist')
            return data, status

        cmd = 'grep "apt upgrade" -B1 /var/log/apt/history.log | tail -2'
        output = subprocess.check_output(cmd, shell=True)

        # example output:
        # Start-Date: 2022-03-18  11:52:49
        # Commandline: apt upgrade
        line = output.splitlines()[0].decode("utf-8")
        s = line.split()
        data['last'] = "{} {}".format(s[1], s[2])
        return data, status
