#!/usr/bin/python

import time
import sys
import os
#from network import NetworkThread
from keylogger import KeyLoggerThread
#from typesetter import TypesetterThread
import traceback

exitFlag = 0
      
if __name__ == "__main__":
    # Create new threads
    #thread1 = myThread(1, "Thread-1", 1)
    #thread2 = myThread(2, "Thread-2", 2)

    #networkCheckerThread = NetworkThread(2)
    keyLoggerThread = KeyLoggerThread()
#    typesetterThread = TypesetterThread("")
    # Make the network checker thread daemonic so we don't have to control it
    #networkCheckerThread.daemon = True
    keyLoggerThread.daemon = True
#    typesetterThread.daemon = True
    # Start new Network checker thread
    #networkCheckerThread.start()
    # start the key loggin thread
    keyLoggerThread.start()
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
