from email import feedparser
from lib.Common.USB.Driver import Driver
import requests

class Processor():
    def __init__(self, deviceID, host="http://localhost", port="8080"):
        self.udev = Driver(deviceID)
        self.host = host
        self.port = port
        self.dataStream = {"UR" : list(),
                           "UL" : list(),
                           "LR" : list(),
                           "LL" : list()}
        self.keys = ["UR", "UL", "LR", "LL"]
        self.upperLimit = 30
    
    def getHost(self):
        return self.host
    def getPort(self):
        return self.port

    def deliver(self):
        for key in self.dataStream.keys():
            for i in range(len(self.dataStream[key])):
                url = self.getHost()+":"+self.getPort()+"/{}/{}".format(key, self.dataStream[key][i])
                try:
                    feedBack = requests.post(url)
                    print("FEEDBACK={}".format(feedBack))
                    self.dataStream[key][i].pop(i) # pop the data we just sent
                except:
                    print("Could not deliver to: {}".format(url))
                    if len(self.dataStream[key]) > self.upperLimit:
                        print("Upper limit reached [{}], purging SEN={}, DATA={}".format(self.upperLimit,
                        key, self.dataStream[key][i]))
                        self.dataStream[key][i].pop(i)

    def process(self):
        data = self.udev.readLine()
        data = data.split(",")
        if len(data) == 4:
            for i in range(len(data)):
                #print("READ: {}, VALUE: int({})".format(self.keys[i], int(data[i])))
                self.dataStream[self.keys[i]].append(data[i])
            self.deliver()


    def cleanUp(self):
        return self.udev.closeConn()
