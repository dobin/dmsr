import requests
import socket
import logging

from client.plugin import Plugin, PluginStatus


class Network():
    def __init__(self):
        self.hostname = socket.gethostname()
        self.password = ''
        self.server = ''


    def send(self, data, status: PluginStatus, plugin):
        headers = {
            'password': self.password,
        }
        packet = {
            'agentname': self.hostname,
            'pluginname': plugin.name,
            'refresh': plugin.refresh,
            'data': data,
            'status': status.value,
            'private': plugin.private,
        }

        try:
            res = requests.post(self.server + '/push', headers=headers, json=packet)
            if res.ok:
                return True
            else:
                logging.warn("Request was not ok")
        except requests.HTTPError as e:
            logging.warn("Error sending HTTP request: {}".format(e.response.status_code))
        except Exception as e:
            logging.warn("Error: {}".format(e))

        return False


    def setConfig(self, server, password):
        self.server = server
        self.password = password


Network = Network()