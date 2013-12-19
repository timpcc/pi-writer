#! /usr/bin/python

import time
import sys
import os
#from network import NetworkThread
from keylogger import KeyLoggerThread
#from typesetter import TypesetterThread
import traceback
import logging

exitFlag = 0

logging.basicConfig(filename="pi-writer.log", level=logging.DEBUG)
logger = logging.getLogger(__name__)
      
if __name__ == "__main__":
    # Create new threads
    #thread1 = myThread(1, "Thread-1", 1)
    #thread2 = myThread(2, "Thread-2", 2)

    #networkCheckerThread = NetworkThread(2)
    logger.debug("Creating threads...")
    keyLoggerThread = KeyLoggerThread()
    logger.debug("KeyLogger thread created")
    # Make the network checker thread daemonic so we don't have to control it
    #networkCheckerThread.daemon = True
    #logger.debug("Network thread created")
    keyLoggerThread.daemon = True
#    typesetterThread.daemon = True
    # Start new Network checker thread
    #networkCheckerThread.start()
    # start the key loggin thread
    keyLoggerThread.start()
    logger.debug("KeyLogger thread started")
#    typesetterThread.start()
    #thread2.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        #networkCheckerThread.stop()
        #networkCheckerThread.join()
        keyLoggerThread.stop()
        keyLoggerThread.join()
        print("Exiting Main Thread")
        sys.exit(0)
    except Exception as e:
        print("Exception: " + str(e))
        #networkCheckerThread.stop()
        #networkCheckerThread.join()
        keyLoggerThread.stop()
        keyLoggerThread.join()
        print("Exiting Main Thread")
        traceback.print_exc(file=sys.stdout)
        sys.exit(0)
