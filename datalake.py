import time


class PluginData():
    def __init__(self, pluginname, refresh, recvTime, data):
        self.pluginname = pluginname
        self.refresh = refresh
        self.recvTime = recvTime
        self.data = data


    def isTimeouted(self):
        if time.time() > self.recvTime + self.refresh * 2:
            return True
        return False


class DataLake():
    def __init__(self):
        self.data = {}


    def push(self, agentname: str, pluginname: str, refresh, data):
        if agentname not in self.data:
            self.data[agentname] = {}

        recvTime = time.time()
        pluginData = PluginData(pluginname, refresh, recvTime, data)
        self.data[agentname][pluginname] = pluginData


    def get(self, agentname: str, pluginname: str) -> PluginData:
        if agentname not in self.data:
            return None
        if pluginname not in self.data[agentname]:
            return None
        return self.data[agentname][pluginname]
    

    def getAll(self):
        return self.data


dataLake = DataLake()