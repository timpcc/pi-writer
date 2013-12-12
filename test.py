'''
Created on 12 Dec 2013

@author: tim.crilly
'''

import time

from Tests.testlogger import TestLoggerThread

if __name__ == "__main__":
    # Create new threads
    testLoggerThread = TestLoggerThread("/home/pi/pi-writer/Tests/testinput1.txt")
    # Start new Network checker thread
    testLoggerThread.start()
    time.sleep(0.1)
    testLoggerThread.join()
    print("Exiting main thread")