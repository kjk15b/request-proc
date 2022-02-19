import sys
from lib.Common.Processor import Processor

if __name__ == '__main__':
    processor = Processor(sys.argv[1])
    processor.process()
    processor.cleanUp()
