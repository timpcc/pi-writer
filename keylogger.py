
#!/usr/bin/python

import threading
import os
import time
import datetime
import shutil
import pyxhook
import json
import ConfigParser
import traceback
import logging
import subprocess
from command import CommandRunner
from textmangler import TextMangler

class KeyLoggerThread(threading.Thread):
    
    def __init__(self):
        super(KeyLoggerThread, self).__init__()
        logging.basicConfig(filename="pi-writer.log", level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        configPath = os.path.join("/home/pi", "pi-writer", "pi-writer.conf")
        self.config = ConfigParser.ConfigParser()
        self.config.read(configPath)
        self.keylogDir = self.config.get("General", "keylogDir")
        #self.commandDir = self.config.get("Logger", "commandDir")
        # self.typesetDir = self.config.get("General", "typesetDir")
        self.commandKey = self.config.get("General", "commandKey")
        self.shutdownKey = self.config.get("General", "shutdownKey")
        self.shutdownKeyHoldTime = self.config.get("General", "shutdownKeyHoldTime")
        self.fileDateFormat = self.config.get("General", "fileDateFormat")
        #self.keylogDir = '/home/pi/pi-writer/current/'
        #self.typesetDir = '/home/pi/pi-writer/typeset/'
        self.hookManager = pyxhook.HookManager()
        self.hookManager.HookKeyboard()
        self.hookManager.KeyDown = self.onKeyDownEvent
        self.hookManager.KeyUp = self.onKeyUpEvent
        self._stop = threading.Event()
        self.pageIndex = 1
        self.startDateTime = datetime.datetime.now().strftime(self.fileDateFormat)
        self.commandMode = False
        self.commandString = ""
        data = self.config.get("Replacements", "patterns")
        self.commandPatterns = self.replaceList = json.loads(data)

    def run(self):
        self.filename = self.createNewWorkingFile()
        self.logger.debug("Writing to new file" + os.path.join(self.keylogDir, self.filename))
        self.hookManager.start()
        while not self._stop.isSet():
            time.sleep(0.1)
        self.logger.debug("Logger thread stopped")
        self.hookManager.cancel()

    def stop(self):
        self.logger.debug("Attempting to stop logger thread...")
        self._stop.set()
        
    def newPage(self):
        # save the current page
        #self.save()
        # increment the page count
        self.writeKey("PageBreak")
        self.pageIndex += 1
        # create a new working file
        #self.filename = self.createNewWorkingFile()
        #print("Writing to new file" + os.path.join(self.keylogDir, self.filename))

    def onKeyUpEvent(self, event):
        if event.Key == self.shutdownKey:
            try:
                self.logger.debug("Cancelling shutdown timer")
                print("Cancelling shutdown timer")
                self.shutdownTimer.cancel()
                self.shutdownTimer.join()
            except:
                self.logger.exception("Exception whilst cancelling shutdown timer")

    def onKeyDownEvent(self, event):
        #print(event.Key)
        
        if event.Key == self.commandKey:
            if self.commandMode:
                # run the command
                self.commandMode = False
                self.executeCommandString()
            else:
                self.commandMode = True
                self.commandString = ""
            return
    
        if event.Key == self.shutdownKey:
            # start timer
            self.logger.debug("Starting shutdown timer")
            print("Starting shutdown timer...")
            self.shutdownTimer = threading.Timer(float(self.shutdownKeyHoldTime), self.shutdown)
            self.shutdownTimer.start()
#        if self._control_l_down and (event.Key == "p" or event.Key == "P"):
#            print("MAKE NEW PAGE")
#            self.newPage()
#            return
        
        #print(str(event.Ascii) + " )Key press: " + event.Key)
        if self.commandMode:
            self.writeKeyToCommand(event.Key)
        else:
            self.writeKey(event.Key)
            
    def writeKey(self, key):
        with open(os.path.join(self.keylogDir, self.filename), 'a') as content_file:
            content_file.write(key + '\n')
            
    def writeKeyToCommand(self, Key):
        self.commandString += Key + '\n'
        
    def executeCommandString(self):
        runner = CommandRunner()
        mangler = TextMangler(self.commandPatterns)
        print("Mangling command: " + self.commandString)
        mangledCommand = mangler.mangle(self.commandString) 
        print("Running command: " + mangledCommand)
        runner.run(mangledCommand)
        print("Command run")
        
    def shutdown(self):
        print("Calling shutdown")
        try:
            # shutdown raspberry pi
            self.logger.debug("Shutting down system")
            print("Shutting down system")
            command = "/usr/bin/sudo /sbin/shutdown now"
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            output = process.communicate()[0]
            self.logger.info(str(output))
        except:
            self.logger.exception("Exception in shutdown timer thread")
            print("Exception in shutdown timer")
            traceback.print_exc()
#    def save(self):
#        print("Saving...")
#        if not os.path.exists(self.typesetDir):
#            os.makedirs(self.typesetDir)
#        print("Working file " + os.path.join(self.keylogDir, self.filename) + " exists " + str(os.path.exists(os.path.join(self.keylogDir, self.filename))))
#        if os.path.exists(os.path.join(self.typesetDir, self.filename)):
#            os.remove(os.path.join(self.typesetDir, self.filename))
#            print("Removed file " + os.path.join(self.typesetDir, self.filename) + ". Source exists " + str(os.path.exists(os.path.join(self.keylogDir, self.filename))))
#        print("Working file " + os.path.join(self.keylogDir, self.filename) + " exists " + str(os.path.exists(os.path.join(self.keylogDir, self.filename))))
#        # move the current working file to the output folder
#        shutil.move(os.path.join(self.keylogDir, self.filename), os.path.join(self.typesetDir, self.filename))
#        print("Moved file to" + os.path.join(self.typesetDir, self.filename))
#        print("File saved")

    def createNewWorkingFile(self):
        count = 2
        d = self.startDateTime
        filename = d + ".tw"
        if not os.path.exists(self.keylogDir):
            os.makedirs(self.keylogDir)
        while os.path.exists(os.path.join(self.keylogDir, filename)):
            filename = d + "_(" + str(count) + ").tw"
            count += 1
            
        return filename
