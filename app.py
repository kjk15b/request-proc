import sys
from lib.Common.Processor.Processor import Processor

if __name__ == '__main__':
    processor = Processor(sys.argv[1])
    countDown = 5
    while countDown > 0 :
        processor.process()
        countDown -= 1
    processor.cleanUp()
