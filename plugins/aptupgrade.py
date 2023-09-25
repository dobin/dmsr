from typing import Tuple, Dict
import os
import subprocess
import logging

from client.plugin import Plugin, PluginStatus


class aptupgrade(Plugin):
    def __init__(self, refresh):
        super().__init__(refresh)


    def run(self) -> Tuple[Dict, PluginStatus]:
        data = {}
        status = PluginStatus.OK
        filepath = '/var/log/apt/history.log'

        if not os.path.exists(filepath):
            status = PluginStatus.ERROR
            logging.error('Plugin aptupgrade: {} does not exist'.format(filepath))
            return data, status

        cmd = 'grep "apt upgrade" -B1 {} | tail -2'.format(filepath)
        output = subprocess.check_output(cmd, shell=True).decode("utf-8")
        # example output:
        # Start-Date: 2022-03-18  11:52:49
        # Commandline: apt upgrade
        lines = output.splitlines()
        if len(lines) < 2:
            logging.warn("No apt upgrade happened")
            data['last'] = 'never'
            status = PluginStatus.INFO
            return data, status

        line = lines[0]
        s = line.split()
        data['last'] = "{} {}".format(s[1], s[2])

        return data, status
