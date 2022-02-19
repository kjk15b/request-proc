from email import feedparser
from lib.Common.USB.Driver import Driver
import requests

class Processor():
    def __init__(self, deviceID, host="http://localhost", port="8080", upperLimit=30):
        self.udev = Driver(deviceID)
        self.host = host
        self.port = port
        self.dataStream = {"UR" : list(),
                           "UL" : list(),
                           "LR" : list(),
                           "LL" : list()}
        self.keys = ["UR", "UL", "LR", "LL"]
        self.upperLimit = int(upperLimit)
        self.thresholds = {"UR" : 1022,
                           "UL" : 1015,
                           "LR" : 1021,
                           "LL" : 1022}
    
    def getHost(self):
        return self.host
    def getPort(self):
        return self.port

    def hitDetected(self, data):
        for i in range(len(data)):
            if data[i] <= self.thresholds[self.keys[i]]:
                return True
        return False

    def deliver(self):
        delivered = False
        for key in self.dataStream.keys():
            for i in range(len(self.dataStream[key])):
                url = self.getHost()+":"+self.getPort()+"/{}/{}".format(key, self.dataStream[key][i])
                try:
                    feedBack = requests.post(url)
                    print("FEEDBACK={}".format(feedBack))
                    delivered = True
                except:
                    print("Could not deliver to: {}".format(url))
                    delivered = False
        if delivered:
            for key in self.dataStream.keys():
                for i in range(len(self.dataStream[key])):
                    self.dataStream[key].pop(i)

    def cleanUpStream(self):
        for key in self.dataStream.keys():
            if len(self.dataStream[key]) > self.upperLimit:
                print("Upper limit [{}] reached, purging {} data {}".format(self.upperLimit,
                        key, self.dataStream[key][0]))
                self.dataStream[key].pop(0)

    def process(self):
        data = self.udev.readLine()
        data = data.split(",")
        if len(data) == 4:
            if self.hitDetected(data):
                for i in range(len(data)):
                    print("READ: {}, VALUE: int({})".format(self.keys[i], int(data[i])))
                    self.dataStream[self.keys[i]].append(data[i])
            self.deliver()
            self.cleanUpStream()


    def cleanUp(self):
        return self.udev.closeConn()
