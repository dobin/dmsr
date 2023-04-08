from flask import Blueprint, current_app, flash, request, redirect, url_for, render_template, make_response, jsonify
from datalake import dataLake
import pprint
import json
import yaml
import logging

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
    else:
        return render_template('login.html')
    

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

    # check if we have all data
    vars = [ 'agentname', 'pluginname', 'refresh', 'data', 'password', 'status' ]
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
    status = packet['status']
    private = packet['private']

    # auth
    if password != current_app.config["PASSWORD"]:
        logging.warn("Invalid password")
        return 'bad request', 400

    # create & finish
    dataLake.push(agentname, pluginname, refresh, data, status, private)
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
