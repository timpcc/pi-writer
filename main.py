#!/usr/bin/python

import time
import sys
import os
from network import NetworkThread
from logger import LoggerThread
from typesetter import TypesetterThread
import traceback

exitFlag = 0
      
if __name__ == "__main__":
    # Create new threads
    #thread1 = myThread(1, "Thread-1", 1)
    #thread2 = myThread(2, "Thread-2", 2)
    
    print("XDG_CONFIG_HOME " + str(os.environ.get("XDG_CONFIG_HOME")))

    networkCheckerThread = NetworkThread(2)
    loggerThread = LoggerThread()
    typesetterThread = TypesetterThread("")
    # Make the network checker thread daemonic so we don't have to control it
    networkCheckerThread.daemon = True
    loggerThread.daemon = True
    typesetterThread.daemon = True
    # Start new Network checker thread
    networkCheckerThread.start()
    # start the key loggin thread
    loggerThread.start()
    typesetterThread.start()
    #thread2.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        networkCheckerThread.stop()
        networkCheckerThread.join()
        loggerThread.stop()
        loggerThread.join()
        print("Exiting Main Thread")
        sys.exit(0)
    except Exception as e:
        print("Exception: " + str(e))
        networkCheckerThread.stop()
        networkCheckerThread.join()
        loggerThread.stop()
        loggerThread.join()
        print("Exiting Main Thread")
        traceback.print_exc(file=sys.stdout)
        sys.exit(0)
