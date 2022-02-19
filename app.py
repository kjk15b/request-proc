import sys
from turtle import up
from lib.Common.Processor.Processor import Processor
import time

if __name__ == '__main__':
    processor = Processor(sys.argv[1], host=sys.argv[2], port=sys.argv[3], upperLimit=sys.argv[4])
    while True :
        processor.process()
        time.sleep(0.1)
    processor.cleanUp()
