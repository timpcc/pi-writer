'''
Created on 11 Dec 2013

@author: tim.crilly
'''
#!/usr/bin/python

import threading
import os
import ConfigParser
import json
import re
from PyRTF import *

class TypesetterThread(threading.Thread):
    
    def __init__(self, path):
        super(TypesetterThread, self).__init__()
        self.publishDir = '/home/pi/pi-writer/publish/'
        self.path = path
        self._stop = threading.Event()
        self.loadSettings()
        
    def loadSettings(self):
        #configPath = os.path.join(os.environ.get("XDG_CONFIG_HOME"), "pi-writer", "typesetter.conf")
        configPath = os.path.join("/home/pi/pi-writer", "typesetter.conf")
        config = ConfigParser.ConfigParser()
        config.read(configPath)
        data = config.get("Replacements", "patterns")
        self.replaceList = json.loads(data)

    def run(self):
        # load the file
        data = ""
        with open(self.path, 'r') as content_file:
            data = content_file.read()
        text = data
        for item in self.replaceList:
            text = re.sub(item["match"], item["replace"], text)
        print(text)

    def stop(self):
        print("Attempting to stop typesetter thread...")
        self._stop.set()
        
    def createRTF(self):
        doc = Document()
        ss = doc.StyleSheet
        section = Section()
        


if __name__ == "__main__":
    typesettingDir = '/home/pi/pi-writer/typeset/'
    files = []
    for (dirpath, dirnames, filenames) in os.walk(typesettingDir):
        files.extend(filenames)
        break
    for file in files:
        typesetterThread = TypesetterThread(os.path.join(typesettingDir, file))
        typesetterThread.start()
        typesetterThread.join()
        
