import time


class PluginData():
    def __init__(self, pluginname, refresh, recvTime, data, status, private):
        self.pluginname = pluginname
        self.refresh = refresh
        self.recvTime = recvTime
        self.data = data
        self.status = status
        self.private = private


    def isTimeouted(self):
        if time.time() > self.recvTime + self.refresh * 2:
            return True
        return False


class DataLake():
    def __init__(self):
        self.data = {}


    def push(self, agentname: str, pluginname: str, refresh, data, status, private):
        if agentname not in self.data:
            self.data[agentname] = {}

        recvTime = time.time()
        pluginData = PluginData(pluginname, refresh, recvTime, data, status, private)
        self.data[agentname][pluginname] = pluginData


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


dataLake = DataLake()