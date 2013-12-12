'''
Created on 12 Dec 2013

@author: tim.crilly
'''

import time

from Tests.testlogger import TestLoggerThread

if __name__ == "__main__":
    # Create new threads
    testLoggerThread = TestLoggerThread()
    # Start new Network checker thread
    testLoggerThread.start("/home/pi/pi-writer/Tests/testinput1.txt")
    time.sleep(0.1)
    testLoggerThread.join()
    print("Exiting main thread")