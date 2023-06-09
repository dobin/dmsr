from flask import Blueprint, current_app, flash, request, redirect, url_for, render_template, make_response, jsonify
import pprint
import json
import yaml
import logging

from datalake import dataLake, PluginData

views = Blueprint('views', __name__)


@views.route("/")
def index():
    isAdmin = checkIsAdmin(request)
    data = dataLake.getAll(isAdmin)
    return render_template('index.html', data=data)


@views.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        pw = request.form['password']
        if pw == current_app.config["ADMINPW"]:
            response = make_response(redirect('/'))
            response.set_cookie('pw', pw)
            return response
        else:
            return redirect('/')
    
    isAdmin = checkIsAdmin(request)
    if isAdmin:
        return render_template('admin.html', isAdmin=isAdmin)
    else:
        return render_template('login.html', isAdmin=isAdmin)


@views.route("/reset", methods=['POST'])
def reset():
    # resets all data (until agents send their next packet)
    # Basically cleans up old inactive agents
    isAdmin = checkIsAdmin(request)
    if isAdmin:
        dataLake.reset()
    return redirect('/')


@views.route("/status")
def status():
    # 200 if all ok,
    # 500 if a plugin warns
    status = dataLake.getStatus()
    if status:
        return make_response('', 200)
    else:
        return make_response('', 500)


def checkIsAdmin(request):
    adminPw = request.cookies.get('pw')
    if adminPw == None:
        return False
    if adminPw == current_app.config["ADMINPW"]:
        return True
    else:
        return False

@views.route("/push", methods=['GET', 'POST'])
def push():
    packet = request.json

    # auth
    password = request.headers.get('password', '')
    if password != current_app.config["PASSWORD"]:
        logging.warn("Invalid password")
        return 'bad request', 400
    
    # check if we have all data
    vars = [ 'agentname', 'pluginname', 'refresh', 'data', 'status', 'private' ]
    for i in vars:
        if not i in packet:
            logging.warn("Missing data")
            return 'bad request', 400       

    # convert
    agentname = packet['agentname']
    pluginname = packet['pluginname']
    refresh = packet['refresh']
    data = packet['data']
    status = packet['status']
    private = packet['private']
    pluginData = PluginData.make(pluginname, refresh, data, status, private)

    # create & finish
    dataLake.push(agentname, pluginData)
    return make_response('', 201)


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
