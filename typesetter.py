'''
Created on 11 Dec 2013

@author: tim.crilly
'''
#!/usr/bin/python

import threading
import os
import ConfigParser
import json

class TypesetterThread(threading.Thread):
    
    def __init__(self, path):
        super(TypesetterThread, self).__init__()
        self.workDir = '/home/pi/pi-writer/current/'
        self.typesetDir = '/home/pi/pi-writer/typeset/'
        self._stop = threading.Event()
        self.loadSettings()
        
    def loadSettings(self):
        #configPath = os.path.join(os.environ.get("XDG_CONFIG_HOME"), "pi-writer", "typesetter.conf")
        configPath = os.path.join("/home/pi/pi-writer", "typesetter.conf")
        config = ConfigParser.ConfigParser()
        config.read(configPath)
        data = config.get("Replacements", "patterns")
        arr = json.loads(data)
        
        print(data)
        print("Len: " + str(len(arr)))
        for item in arr:
            print(item.match)
            print(item.replace)
            print("----")

    def run(self):
        self.filename = self.createNewWorkingFile()
        
        print("Writing to new file" + os.path.join(self.workDir, self.filename))
        self.hookManager.start()
        while not self._stop.isSet():
            time.sleep(0.1)
        print("Logger thread stopped")
        self.hookManager.cancel()

    def stop(self):
        print("Attempting to stop typesetter thread...")
        self._stop.set()

    def sendEmail(self, content):
        fromaddr = 'tim.crilly@gmail.com'
        toaddrs  = 'tim.crilly@boardworks.co.uk'
        msg = content
        username = 'tim.crilly@gmail.com'
        password = 'C0ffeecup'
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username,password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
