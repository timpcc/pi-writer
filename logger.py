#!/usr/bin/python

import threading
import os
import smtplib
import time
import datetime
import shutil
import pyxhook

class LoggerThread(threading.Thread):
    
    def __init__(self):
        super(LoggerThread, self).__init__()
        self.workDir = '/home/pi/pi-writer/current/'
        self.typesetDir = '/home/pi/pi-writer/typeset/'
        self.hookManager = pyxhook.HookManager()
        self.hookManager.HookKeyboard()
        self.hookManager.KeyDown = self.onKeyDownEvent
        self.hookManager.KeyUp = self.onKeyUpEvent
        self._stop = threading.Event()
        self.pageIndex = 1
        self.startDateTime = datetime.datetime.now().strftime("%Y%m%d_%H.%M.%S")
        self._control_l_down = False
        

    def run(self):
        self.filename = self.createNewWorkingFile()
        
        print("Writing to new file" + os.path.join(self.workDir, self.filename))
        self.hookManager.start()
        while not self._stop.isSet():
            time.sleep(0.1)
        print("Logger thread stopped")
        self.hookManager.cancel()

    def stop(self):
        print("Attempting to stop logger thread...")
        self._stop.set()
        
    def newPage(self):
        # save the current page
        #self.save()
        # increment the page count
        self.writeKey("PageBreak")
        self.pageIndex += 1
        # create a new working file
        #self.filename = self.createNewWorkingFile()
        #print("Writing to new file" + os.path.join(self.workDir, self.filename))

    def onKeyUpEvent(self, event):
        if event.Key == "Control_L" and self._control_l_down:
            self._control_l_down = False

    def onKeyDownEvent(self, event):
        print(event.Key)
        if event.Key == "Control_L":
            self._control_l_down = True
        if self._control_l_down and (event.Key == "p" or event.Key == "P"):
            print("MAKE NEW PAGE")
            self.newPage()
            return
        
        #print(str(event.Ascii) + " )Key press: " + event.Key)
        self.writeKey(event.Key)
            
    def writeKey(self, key):
        with open(os.path.join(self.workDir, self.filename), 'a') as content_file:
            content_file.write(key + '\n')
            
    def save(self):
        print("Saving...")
        if not os.path.exists(self.typesetDir):
            os.makedirs(self.typesetDir)
        print("Working file " + os.path.join(self.workDir, self.filename) + " exists " + str(os.path.exists(os.path.join(self.workDir, self.filename))))
        if os.path.exists(os.path.join(self.typesetDir, self.filename)):
            os.remove(os.path.join(self.typesetDir, self.filename))
            print("Removed file " + os.path.join(self.typesetDir, self.filename) + ". Source exists " + str(os.path.exists(os.path.join(self.workDir, self.filename))))
        print("Working file " + os.path.join(self.workDir, self.filename) + " exists " + str(os.path.exists(os.path.join(self.workDir, self.filename))))
        # move the current working file to the output folder
        shutil.move(os.path.join(self.workDir, self.filename), os.path.join(self.typesetDir, self.filename))
        print("Moved file to" + os.path.join(self.typesetDir, self.filename))
        print("File saved")

    def createNewWorkingFile(self):
        count = 2
        d = self.startDateTime
        filename = d + ".tw"
        if not os.path.exists(self.workDir):
            os.makedirs(self.workDir)
        while os.path.exists(os.path.join(self.workDir, filename)):
            filename = d + "_(" + str(count) + ").tw"
            count += 1
            
        return filename
