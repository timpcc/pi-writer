#! /usr/bin/python
'''
Created on 11 Dec 2013

@author: tim.crilly
'''
#!/usr/bin/python

import os
import sys
import ConfigParser
import json
import unicodedata
import shutil
import datetime
import tarfile
import logging
from PyRTF import *
from mailer import Mailer
from textmangler import TextMangler

class Typesetter():
    
    def __init__(self):
        self.log = logging.getLogger(__name__)
        
        self.rtfFiles = []
        self.loadSettings()
        
    def loadSettings(self):
        #configPath = os.path.join(os.environ.get("XDG_CONFIG_HOME"), "pi-writer", "typesetter.conf")
        configPath = os.path.join("/home/pi/pi-writer", "pi-writer.conf")
        self.config = ConfigParser.ConfigParser()
        self.config.read(configPath)
        self.fileDateFormat = self.config.get("General", "fileDateFormat")
        data = self.config.get("Replacements", "patterns")
        self.keylogDir = self.config.get("General", "keylogDir")
        self.publishDir = self.config.get("General", "publishDir")
        
        self.archiveDir = self.config.get("General", "archiveDir")
        print(data)
        self.replaceList = json.loads(data)
        
    def getFiles(self):
        self.files = []
        for (dirpath, dirnames, filenames) in os.walk(self.keylogDir):
            for f in filenames:
                self.files.append(os.path.join(dirpath, f))
            break;
        return len(self.files) > 0
        
    def run(self):
        if self.getFiles():
            if self.process() is not None:
                archive = self.archive(self.files)
                if archive is not None:
                    print("Working files archived to " + archive)
                    return True
        return False

    def process(self):
        try:
            # load the files
            for f in self.files:
                try:
                    data = ""
                    with open(f, 'r') as content_file:
                        data = content_file.read()
                        text = data
                        mangler = TextMangler(self.replaceList)
                        text = mangler.mangle(text)
                
                    doc = self.createRTFDocument(text)
                    renderer = Renderer()
                
                    (directory, filename) = os.path.split(f)
                
                    if not os.path.exists(self.publishDir):
                        os.makedirs(self.publishDir)
                    
                    rtfName = os.path.join(self.publishDir, filename + '.rtf')
                        
                    renderer.Write(doc, open(rtfName, 'w'))
                    self.rtfFiles.append(rtfName)
                except Exception as rtfE:
                    print(str(rtfE))
                    continue
            return self.rtfFiles
        except Exception as e:
            print(str(e))
            return None
        
    def archive(self, files):
        try:
            # copy the files to a temp directory
            fname = datetime.datetime.now().strftime(self.fileDateFormat)
            target = os.path.join(self.archiveDir, fname + ".tar.gz")
            tar = tarfile.open(target, "w:gz")
            for f in files:
                tar.add(f)
            tar.close()
            for f2 in files:
                try:
                    os.remove(f2)
                except OSError as ose:
                    print("Failed to delete " + f2 + " due to: " + str(ose))
            return target
        except Exception as e:
            print(str(e))
            return None
        
        
    def createRTFDocument(self, text):
        doc = Document()
        ss = doc.StyleSheet
        section = Section()
        doc.Sections.append(section)
        paras = text.split('\n')
               
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


def archiveToDir(sentDir, files):
    try:
        # copy the files to a temp directory
        fname = datetime.datetime.now().strftime(self.fileDateFormat)
        if not os.path.exists(sentDir):
                os.makedirs(sentDir)
        target = os.path.join(self.sentDir, fname + ".tar.gz")
        tar = tarfile.open(target, "w:gz")
        for f in files:
            tar.add(f)
        tar.close()
        for f2 in files:
            try:
                os.remove(f2)
            except OSError as ose:
                print("Failed to delete " + f2 + " due to: " + str(ose))
        return target
    except Exception as e:
        print(str(e))
        return None

if __name__ == "__main__":
    log = logging.getLogger(__name__)
    configPath = os.path.join("/home/pi/pi-writer", "pi-writer.conf")
    config = ConfigParser.ConfigParser()
    config.read(configPath)
    publishDir = config.get("General", "publishDir")
    sentDir = config.get("General", "sentDir")
    
    typesetter = Typesetter()

    if typesetter.run():        
        # Email files
        print("Typesetter run successfully")
        
    # get all the files in the publish folder and email them
    files = []
    for (dirpath, dirnames, filenames) in os.walk(publishDir):
        for f in filenames:
            files.append(os.path.join(dirpath, f))
            break;
    
    print("There are " + len(files) + " published files to email")
    if len(files) > 0:
        mailer = Mailer()
        
        if (mailer.send("Tests", "See Attackmented Text File(s)", files)):            
            # move the file to the sent directory
            archiveToDir(sentDir, files)
                
                

    
   # for file in files:
   #     typesetterThread = Typesetter(os.path.join(inputDir, file))
   #     typesetterThread.start()
   #     typesetterThread.join()
        
