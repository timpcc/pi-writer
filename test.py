'''
Created on 12 Dec 2013

@author: tim.crilly
'''
from Tests.testlogger import TestLoggerThread

if __name__ == "__main__":
    # Create new threads
    testLoggerThread = TestLoggerThread()
    # Start new Network checker thread
    testLoggerThread.start("/home/pi/pi-writer/Tests/testinput1.txt")
    print("Exiting main thread")