from email import feedparser
from lib.Common.USB.Driver import Driver
import requests

class Processor():
    def __init__(self, deviceID, host="localhost", port="8080", upperLimit=30):
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
    '''
    getHost
    return host
    '''
    def getHost(self):
        return self.host
    
    '''
    getPort
    return port as str
    '''
    def getPort(self):
        return self.port
    
    '''
    hitDetected
    Check if any of data reached their threshold,
    return bool / True / Fals
    '''
    def hitDetected(self, data):
        for i in range(len(data)):
            if int(data[i]) <= self.thresholds[self.keys[i]]:
                return True
        return False

    '''
    deliver
    attempt to deliver datastream to host
    if unsuccessful, keep backups in a backup stream
    purge delivered contents and swap streams
    '''
    def deliver(self):
        backupStream = self.dataStream # swap streams to be sure we clean out things
        for key in self.dataStream.keys():
            for i in range(len(self.dataStream[key])):
                url = "http://"+self.getHost()+":"+self.getPort()+"/{}/{}".format(key, self.dataStream[key][i])
                try:
                    feedBack = requests.post(url)
                    print("FEEDBACK={}".format(feedBack))
                    backupStream[key].pop(i)
                except:
                    print("Could not deliver to: {}".format(url))
        self.dataStream = backupStream # replace streams

    '''
    cleanUpStream
    check if over the upperLimit defined at run-time
    '''
    def cleanUpStream(self):
        for key in self.dataStream.keys():
            if len(self.dataStream[key]) > self.upperLimit:
                print("Upper limit [{}] reached, purging {} data {}".format(self.upperLimit,
                        key, self.dataStream[key][0]))
                self.dataStream[key].pop(0)

    '''
    process
    Read injest data and and check if it needs to be delivered
    '''
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

    '''
    cleanUp
    close the USB connection
    '''
    def cleanUp(self):
        return self.udev.closeConn()
