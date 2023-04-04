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


def loadPlugins(config, globalRefresh: int):
    plugins = []

    for pluginName in config:
        pluginConfig = config[pluginName]

        # skip inactive
        if not ('enabled' in pluginConfig and pluginConfig['enabled']):
            continue

        plugin = loadPlugin(pluginName, config, globalRefresh)
        plugins.append(plugin)

    return plugins


def loadPlugin(pluginName, config, globalRefresh):
    module = importlib.import_module('plugins.' + pluginName)
    p = getattr(module, pluginName)
    pluginConfig = config[pluginName]
    plugin = p(refresh=globalRefresh)
    plugin.setConfig(pluginConfig)
    return plugin


def loadConfig():
    with open('agent.yaml') as f:
        yamlData = yaml.safe_load(f)
        config = yamlData
        return config


def executor(plugin, verbose=False):
    data, status = plugin.run()
    try:
        Network.send(data, plugin.name, plugin.refresh, status)
        if verbose:
            print("Sending data from plugin {} successful: {}".format(plugin.name, data))
    except:
        logging.info("Could not reach server, ignoring")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', type=str, help='A single plugin to test (does not send data)')
    args = parser.parse_args()
    config = loadConfig()
    Network.setConfig(config['server'], config['password'])
    
    if args.test:
        plugin = loadPlugin(args.test, config['plugins'], config['refresh'])
        print("Plugin {} (refresh: {})".format(plugin.name, plugin.refresh))
        data = plugin.run()
        pprint.pprint(data, indent=4)

    else:
        plugins = loadPlugins(config['plugins'], config['refresh'])
        for plugin in plugins:
            print("Plugin {} (refresh: {})".format(plugin.name, plugin.refresh))
            executor(plugin, verbose=True)
            schedule.every(plugin.refresh).seconds.do(executor, plugin)

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    main()