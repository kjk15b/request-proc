from lib.Common.USB.Driver import Driver

class Processor():
    def __init__(self, deviceID, endpoint="http://localhost", port="8080"):
        self.udev = Driver(deviceID)
        self.endpoint = endpoint
        self.port = port

    def process(self):
        print(self.udev.readLine())

    def cleanUp(self):
        return self.udev.closeConn()
