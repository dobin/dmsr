#!/usr/bin/python3

import os
import importlib
import logging
import time
import schedule
import yaml
from typing import List

from client.network import Network


def loadPlugins(pluginConfig, globalRefresh: int):
    plugins = []

    for pluginName in pluginConfig:
        config = pluginConfig[pluginName]

        # skip inactive
        if not ('enabled' in config and config['enabled']):
            continue

        # load plugin
        module = importlib.import_module('plugins.' + pluginName)
        p = getattr(module, pluginName)
        
        # configure it
        plugin = p(refresh=globalRefresh)
        plugin.setConfig(config)
        if 'refresh' in config:
            plugin.refresh = config['refresh']
            
        plugins.append(plugin)

    return plugins


def loadConfig():
    with open('agent.yaml') as f:
        yamlData = yaml.safe_load(f)
        config = yamlData
        print("Config: {}".format(yamlData))
        return config


def main():
    config = loadConfig()
    Network.setConfig(config['server'], config['password'])
    plugins = loadPlugins(config['plugins'], config['refresh'])

    for plugin in plugins:
        print("Plugin {} refresh: {}".format(plugin.name, plugin.refresh))
        plugin.run()
        schedule.every(plugin.refresh).seconds.do(plugin.run)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()