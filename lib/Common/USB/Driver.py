import serial

class Driver():
    def __init__(self, deviceID):
        try:
            self.conn = serial.Serial(deviceID,
            baudrate=9600)
        except:
            print("Error connecting to serial device: {}".format(deviceID))

    '''
    readLine
    read line from USB, decode as UTF-8 string
    '''
    def readLine(self):
        try:
            return str(self.conn.readline().decode('utf-8'))
        except:
            print("Error reading line")
            return -1
    
    '''
    closeConn
    close the current connection
    '''
    def closeConn(self):
        try:
            return self.conn.close()
        except:
            print("Error closing device")
            return -1
