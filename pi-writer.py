#! /usr/bin/python

import time
import sys
import os
#from network import NetworkThread
from keylogger import KeyLoggerThread
#from typesetter import TypesetterThread
import traceback
import logging
import daemon

class PiWriterDaemon(daemon.Daemon):
    
    def run(self):
        logging.basicConfig(filename="/var/log/pi-writer/pi-writer.log", level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")
        logger = logging.getLogger(__name__)
        # Create new threads
        logger.debug("Creating threads...")
        keyLoggerThread = KeyLoggerThread()
        logger.debug("KeyLogger thread created")
        keyLoggerThread.daemon = True
        # start the key loggin thread
        keyLoggerThread.start()
        logger.debug("KeyLogger thread started")
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            keyLoggerThread.stop()
            keyLoggerThread.join()
            logger.info("Exiting Main thread due to Keyboard interrupt.")
            sys.exit(0)
        except Exception as e:
            logger.exception("Exception in main thread")
            keyLoggerThread.stop()
            keyLoggerThread.join()
            logger.warn("Exiting Main thread due to exception.")


      
if __name__ == "__main__":
    daemon = PiWriterDaemon('/tmp/pi-writer-daemon-example.pid', stdout="/home/pi/stdout.log", stderr="/home/pi/stderr.log")
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
    
