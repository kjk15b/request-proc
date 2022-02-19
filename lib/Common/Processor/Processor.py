from lib.Common.USB.Driver import Driver

class Processor():
    def __init__(self, deviceID, endpoint="http://localhost", port="8080"):
        self.udev = Driver(deviceID)
        self.endpoint = endpoint
        self.port = port
        self.dataStream = {"UR" : list(),
                           "UL" : list(),
                           "LR" : list(),
                           "LL" : list()}
        self.keys = ["UR", "UL", "LR", "LL"]
    
    def process(self):
        data = self.udev.readLine()
        data = data.split(",")
        if len(data) == 4:
            for i in range(len(data)):
                print("READ: {}, VALUE: int({})".format(self.keys[i], int(data[i])))

    def cleanUp(self):
        return self.udev.closeConn()
