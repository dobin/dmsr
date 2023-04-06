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
        filepath = '/var/log/apt/history.log'

        if not os.path.exists(filepath):
            status = 'error'
            logging.error('Plugin aptupgrade: {} does not exist'.format(filepath))
            return data, status

        cmd = 'grep "apt upgrade" -B1 {} | tail -2'.format(filepath)
        output = subprocess.check_output(cmd, shell=True).decode("utf-8")
        # example output:
        # Start-Date: 2022-03-18  11:52:49
        # Commandline: apt upgrade
        line = output.splitlines()[0]
        s = line.split()
        data['last'] = "{} {}".format(s[1], s[2])

        return data, status
