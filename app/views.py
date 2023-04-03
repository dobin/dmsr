from flask import Blueprint, current_app, flash, request, redirect, url_for, render_template, make_response, jsonify
from datalake import dataLake
import pprint
import json
import yaml
import logging

views = Blueprint('views', __name__)


@views.route("/")
def index():
    data = dataLake.getAll()
    return render_template('index.html', data=data)


@views.route("/push", methods=['GET', 'POST'])
def push():
    packet = request.json

    # check if we have all data
    vars = 'agentname', 'pluginname', 'refresh', 'data', 'password'
    for i in vars:
        if not i in packet:
            logging.warn("Missing data")
            return 'bad request', 400       

    # convert
    agentname = packet['agentname']
    pluginname = packet['pluginname']
    refresh = packet['refresh']
    data = packet['data']
    password = packet['password']

    # auth
    if password != current_app.config["PASSWORD"]:
        logging.warn("Invalid password")
        return 'bad request', 400

    # create & finish
    dataLake.push(agentname, pluginname, refresh, data)
    ret = { 'success': 'true'}
    return make_response(jsonify(ret), 201)


@views.app_template_filter('prettyjson')
def prettyjson_filter(s):
    s = yaml.dump(s, default_flow_style=False)
    ret = []
    # add some newlines
    for line in s.splitlines():
        if line[0].isalnum():
            line = "\n" + line
        ret.append(line)
    return '\n'.join(ret)
