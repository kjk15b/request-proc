import sys
from lib.Common.Processor.Processor import Processor
import time

if __name__ == '__main__':
    processor = Processor(sys.argv[1])
    while True :
        processor.process()
        time.sleep(0.1)
    processor.cleanUp()
