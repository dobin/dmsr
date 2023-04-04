#!/usr/bin/python3

import os
import importlib
import logging
import time
import schedule
import yaml
import argparse
import pprint
from typing import List

from client.network import Network


def loadPlugins(pluginConfig, globalRefresh: int):
    plugins = []

    for pluginName in pluginConfig:
        config = pluginConfig[pluginName]

        # skip inactive
        if not ('enabled' in config and config['enabled']):
            continue

        plugin = loadPlugin(pluginName, globalRefresh)
        plugin.setConfig(config)
        plugins.append(plugin)

    return plugins


def loadPlugin(pluginName, globalRefresh):
    module = importlib.import_module('plugins.' + pluginName)
    p = getattr(module, pluginName)
    plugin = p(refresh=globalRefresh)
    return plugin


def loadConfig():
    with open('agent.yaml') as f:
        yamlData = yaml.safe_load(f)
        config = yamlData
        return config


def executor(plugin):
    data = plugin.run()
    try:
        Network.send(data, plugin.name, plugin.refresh)
    except:
        logging.info("Could not reach server, ignoring")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', type=str, help='A single plugin to test (does not send data)')
    args = parser.parse_args()
    config = loadConfig()
    Network.setConfig(config['server'], config['password'])
    
    if args.test:
        plugin = loadPlugin(args.test, config['refresh'])
        print("Plugin {} (refresh: {})".format(plugin.name, plugin.refresh))
        data = plugin.run()
        pprint.pprint(data, indent=4)

    else:
        plugins = loadPlugins(config['plugins'], config['refresh'])
        for plugin in plugins:
            print("Plugin {} (refresh: {})".format(plugin.name, plugin.refresh))
            plugin.run()
            schedule.every(plugin.refresh).seconds.do(executor, plugin)

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    main()