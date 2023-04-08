import requests
import socket
import logging


class Network():
    def __init__(self):
        self.hostname = socket.gethostname()
        self.password = ''
        self.server = ''


    def send(self, data, status, plugin):
        packet = {
            'agentname': self.hostname,
            'pluginname': plugin.name,
            'refresh': plugin.refresh,
            'password': self.password,
            'data': data,
            'status': status,
            'private': plugin.private,
        }

        try:
            res = requests.post(self.server + '/push', json=packet)
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