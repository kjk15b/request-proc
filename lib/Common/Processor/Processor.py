from lib.Common.USB.Driver import Driver
import requests
import datetime

class Processor():
    def __init__(self, deviceID, host="localhost", port="8080", upperLimit=30):
        self.udev = Driver(deviceID)
        self.host = host
        self.port = port
        self.dataStream = {"UR" : list(),
                           "UL" : list(),
                           "LR" : list(),
                           "LL" : list()}
        self.outStream = {"UR" : list(),
                           "UL" : list(),
                           "LR" : list(),
                           "LL" : list()}
        self.keys = ["UR", "UL", "LR", "LL"]
        self.upperLimit = int(upperLimit)
        self.thresholds = {"UR" : 1022,
                           "UL" : 1015,
                           "LR" : 1021,
                           "LL" : 1022}
        self.timeStart = datetime.datetime.utcnow()
        self.timeStart = self.timeStart.timestamp()

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
    findFrequency
    loop over lists of raw data,
    count how many are below threshold
    divide by time-delta
    '''
    def findFrequency(self):
        for key in self.dataStream.keys():
            hitsCounted = 0
            for i in range(len(self.dataStream[key])):
                if int(self.dataStream[key][i]) <= self.thresholds[key]:
                    hitsCounted += 1
            utcNow = datetime.datetime.utcnow()
            utcNow = utcNow.timestamp()
            theFreq = None
            if utcNow - self.timeStart == 0:
                theFreq = 0
            else:
                theFreq = round(hitsCounted / (utcNow - self.timeStart), 5)
            self.outStream[key].append(theFreq)
            print("Frequency for sensor {} {} Hz".format(key, theFreq))

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
        backupStream = self.outStream # swap streams to be sure we clean out things
        for key in self.outStream.keys():
            for i in range(len(self.outStream[key])):
                url = "http://"+self.getHost()+":"+self.getPort()+"/data/ingest/{}".format(key)
                try:
                    feedBack = requests.post(url, data={'data' : self.outStream[key][i]})
                    feedBack.elapsed
                    feedBack.headers
                    feedBack.request
                    feedBack.status_code
                    print("FEEDBACK=\n \
                        \tStatus={}\n \
                        \tHeaders={}\n \
                        \tElapsed={}\n \
                        \tRequest={}".format(feedBack.status_code, feedBack.headers,
                        feedBack.elapsed, feedBack.request.body))
                    backupStream[key].pop(i)
                except:
                    print("Could not deliver to: {}".format(url))
        self.outStream = backupStream # replace streams

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
            if len(self.outStream[key]) > self.upperLimit:
                print("Upper limit [{}] reached, purging {} data {}".format(self.upperLimit,
                        key, self.outStream[key][0]))
                self.outStream[key].pop(0)

    '''
    process
    Read injest data and and check if it needs to be delivered
    '''
    def process(self):
        data = self.udev.readLine()
        try:
            data = data.split(",")
            if len(data) == 4:
                if self.hitDetected(data):
                    for i in range(len(data)):
                        print("READ: {}, VALUE: int({})".format(self.keys[i], int(data[i])))
                        self.dataStream[self.keys[i]].append(data[i])
                self.deliver()
                self.cleanUpStream()
        except:
            print("Error trying to split int object... skipping")
        self.findFrequency()
    '''
    cleanUp
    close the USB connection
    '''
    def cleanUp(self):
        return self.udev.closeConn()
