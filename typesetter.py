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
import unicodedata
from PyRTF import *
from mailer import Mailer

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
        print(data)
        self.replaceList = json.loads(data)

    def run(self):
        # load the file
        data = ""
        with open(self.path, 'r') as content_file:
            data = content_file.read()
        text = data
        for item in self.replaceList:
            text = re.sub(item["match"], item["replace"], text)
        #print(text)
        
        doc = self.createRTFDocument(text)
        renderer = Renderer()
        
        (directory, filename) = os.path.split(self.path)
        
        if not os.path.exists(self.publishDir):
            os.makedirs(self.publishDir)
        
        rtf_file_name = os.path.join(self.publishDir, filename + '.rtf')
            
        renderer.Write(doc, open(rtd_file_name, 'w'))
            
        mailer = Mailer()
        mailer.send("Tests", "See Attackmented Text File", [rtf_file_name])

    def stop(self):
        print("Attempting to stop typesetter thread...")
        self._stop.set()
        
    def createRTFDocument(self, text):
        doc = Document()
        ss = doc.StyleSheet
        section = Section()
        doc.Sections.append(section)
        paras = text.split(']')
        
#        index = 1
#        for par in paras:
#            if par == "":
#                print("Skip emailing empty paragraph")
#                continue     
#            mailer = Mailer()
#            mailer.send("Paragraph " + str(index), par)
#            index += 1
        
        first = True
        for pt in paras:
            if pt == "":
                print("Skipping empty paragraph")
                continue            
            cls = pt.__class__

            print("Paragraph type: " + str(cls))
            if str(type(pt)) == "<type 'unicode'>":
                print("Normalizing unicode")
                text = unicodedata.normalize("NFKD", pt).encode('ascii', 'ignore')
            else:
                print("Text already ASCII")
                text = pt
            if first:
                p = Paragraph(ss.ParagraphStyles.Normal)
                first = False
            else:
                p = Paragraph()
            p.append(TEXT( text, font=ss.Fonts.VTPortableRemington ))
            section.append(p)
        return doc


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
        
