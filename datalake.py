import time
import logging

from client.plugin import PluginStatus


class PluginData():
    def __init__(self, pluginname: str, refresh: int, recvTime, data, status: PluginStatus, private: bool):
        self.pluginname: str = pluginname
        self.refresh: int = refresh
        self.recvTime = recvTime
        self.data = data
        self.status: PluginStatus = status
        self.private: bool = private


    def isTimeouted(self):
        if time.time() > self.recvTime + self.refresh * 2:
            return True
        return False
    

    @staticmethod 
    def make(pluginname, refresh, data, status, private):
        recvTime = time.time()
        return PluginData(pluginname, refresh, recvTime, data, status, private)
    

class DataLake():
    def __init__(self):
        self.data = {}


    def reset(self):
        self.data = {}


    def push(self, agentname: str, pluginData):
        if agentname not in self.data:
            self.data[agentname] = {}

        self.data[agentname][pluginData.pluginname] = pluginData


    def get(self, agentname: str, pluginname: str) -> PluginData:
        if agentname not in self.data:
            return None
        if pluginname not in self.data[agentname]:
            return None
        return self.data[agentname][pluginname]
    

    def getAll(self, isAdmin=False):
        if isAdmin:
            return self.data

        ret = {}
        for agentName in self.data:
            ret[agentName] = {}
            for pluginName in self.data[agentName]:
                if not self.data[agentName][pluginName].private:
                    ret[agentName][pluginName] = self.data[agentName][pluginName]
        return ret
    

    def getStatus(self):
        for agentName in self.data:
            for pluginName in self.data[agentName]:
                if self.data[agentName][pluginName].status != '':
                    logging.info("Status: {} {} {}".format(agentName, pluginName, self.data[agentName][pluginName].status))
                    return False
        return True


dataLake = DataLake()