from typing import Tuple, Dict
import os
import subprocess
import logging
import glob

from client.plugin import Plugin


class filecount(Plugin):
    def __init__(self, refresh):
        super().__init__(refresh)
        self.config['observed'] = []


    def run(self) -> Tuple[Dict, str]:
        data = {}
        status = ''

        for observ in self.config["observed"]:
            name = observ["name"]
            globStr = observ["glob"]

            files = glob.glob(f"{globStr}")
            data[name] = len(files)

        return data, status
