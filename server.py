#!/usr/bin/python3

import os
import argparse
from flask import Flask
import yaml

from app.views import views
from datalake import dataLake


def initTestData():
    data = { 'data': 'test 1', 'more': { 'stuff': 'bla'}}
    dataLake.push('agent1', 'plugin1', 3, data)

    data = { 'data': 'test 2'}
    dataLake.push('agent1', 'plugin2', 3, data)

    data = { 'data': 'test 3'}
    dataLake.push('agent2', 'plugin1', 60, data)


def loadConfig():
    with open('server.yaml') as f:
        yamlData = yaml.safe_load(f)
        config = yamlData
        print("Config: {}".format(yamlData))
        return config
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--listenip', type=str, help='IP to listen on', default="0.0.0.0")
    parser.add_argument('--listenport', type=int, help='Port to listen on', default=5000)
    args = parser.parse_args()

    root_folder = os.path.dirname(__file__)
    app_folder = os.path.join(root_folder, 'app')
	
    app = Flask(__name__,
        static_folder=os.path.join(app_folder, 'static'),
		template_folder=os.path.join(app_folder, 'templates'))
    app.register_blueprint(views)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SESSION_TYPE'] = 'filesystem'

    #initTestData()
    config = loadConfig()
    app.config['PASSWORD'] = config['password']
    app.config['PAGEREFRESH'] = config['pagerefresh']

    app.run(host=args.listenip,
            port=args.listenport)
