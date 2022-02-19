import serial

class Driver():
    def __init__(self, deviceID):
        try:
            self.conn = serial.Serial(deviceID,
            baudrate=9600)
        except:
            print("Error connecting to serial device: {}".format(deviceID))

    def readLine(self):
        return self.conn.readline().encode('utf-8')

    def closeConn(self):
        return self.conn.close()