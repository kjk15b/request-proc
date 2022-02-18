import sys
import serial

if __name__ == '__main__':
    conn = serial.Serial(sys.argv[1], baudrate=9600)
    feedBack = conn.readline()
    print("Found={}".format(feedBack))
    conn.close()
