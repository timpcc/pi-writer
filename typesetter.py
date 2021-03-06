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
import traceback
import tarfile
import logging
from PyRTF import *
from mailer import Mailer
from textmangler import TextMangler

class Typesetter():
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)        
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
        self.replaceList = json.loads(data)
        
    def getFiles(self):
        try:
            self.files = []
            for (dirpath, dirnames, filenames) in os.walk(self.keylogDir):
                for f in filenames:
                    self.files.append(os.path.join(dirpath, f))
                break;
            return len(self.files) > 0
        except:
            #traceback.print_exc(file=sys.stdout)
            self.logger.exception("Exception whilst getting files to typeset")
            return False
        
    def run(self):
        try:
            self.logger.info("Running typesetter")
            if self.getFiles():
                if self.process() is not None:
                    archive = self.archive(self.files)
                    if archive is not None:
                        self.logger.info("Working files archived to " + archive)
                        return True
                    else:
                        self.logger.info("Failed to archive keylog files")
                else:
                    self.logger.info("Failed to typeset files")
            else:
                self.logger.info("There are no files in '" + self.keylogDir + "' to typeset")
                return False
        except:
            #traceback.print_exc(file=sys.stdout)
            self.logger.exception("Exception wilst running typesetter")
            return False

    def process(self):
        try:
            self.logger.info("There are " + str(len(self.files)) + " to typeset")
            # load the files
            for f in self.files:
                try:
                    self.logger.info("Typesetting: " + f)
                    data = ""
                    with open(f, 'r') as content_file:
                        data = content_file.read()
                        text = data
                        mangler = TextMangler(self.replaceList)
                        text = mangler.mangle(text)
                
                    doc = self.createRTFDocument(text)
                    if doc is None:
                        self.logger.info("Failed to create rtf document")
                        return None;
                    renderer = Renderer()
                
                    (directory, filename) = os.path.split(f)
                
                    if not os.path.exists(self.publishDir):
                        os.makedirs(self.publishDir)
                    
                    rtfName = os.path.join(self.publishDir, filename + '.rtf')
                        
                    renderer.Write(doc, open(rtfName, 'w'))
                    self.logger.info("typeset to RTF document: " + rtfName)
                    self.rtfFiles.append(rtfName)
                except:
                    #traceback.print_exc(file=sys.stdout)
                    self.logger.exception("Exception whilst processing file")
                    continue
            return self.rtfFiles
        except:
            self.logger.exception("Exception whilst processing keylogs")
            #traceback.print_exc(file=sys.stdout)
            return None
        
    def archive(self, files):
        try:
            # copy the files to a temp directory
            if not os.path.exists(self.archiveDir):
                os.makedirs(self.archiveDir)
            fname = datetime.datetime.now().strftime(self.fileDateFormat)
            target = os.path.join(self.archiveDir, fname + ".tar.gz")
            tar = tarfile.open(target, "w:gz")
            for f in files:
                fn = os.path.basename(f)
                tar.add(f, fn)
            tar.close()
            for f2 in files:
                try:
                    os.remove(f2)
                except OSError as ose:
                    self.logger.exception("Failed to delete " + f2 + " due to: " + str(ose))
            return target
        except:
            self.logger.exception("Exception whilst archiving files")
            #traceback.print_exc(file=sys.stdout)
            return None
        
        
    def createRTFDocument(self, text):
        try:
            doc = Document()
            ss = doc.StyleSheet
            section = Section()
            doc.Sections.append(section)
            paras = text.split('\n')
                   
            first = True
            for pt in paras:
                if pt == "":
                    continue            
                cls = pt.__class__

                if str(type(pt)) == "<type 'unicode'>":
                    text = unicodedata.normalize("NFKD", pt).encode('ascii', 'ignore')
                else:
                    text = pt
                if first:
                    p = Paragraph(ss.ParagraphStyles.Normal)
                    first = False
                else:
                    p = Paragraph()
                p.append(TEXT( text, font=ss.Fonts.VTPortableRemington ))
                section.append(p)
            return doc
        except:
            #traceback.print_exc(file=sys.stdout)
            self.logger.exception("Exception whilst creating RTF document")
            return None;


def archiveToDir(sentDir, files):
    try:
        # copy the files to a temp directory
        fname = datetime.datetime.now().strftime("%Y%m%d_%H.%M.%S")
        if not os.path.exists(sentDir):
                os.makedirs(sentDir)
        target = os.path.join(sentDir, fname + ".tar.gz")
        tar = tarfile.open(target, "w:gz")
        for f in files:
            tar.add(f)
        tar.close()
        for f2 in files:
            try:
                os.remove(f2)
            except OSError as ose:
                log.exception("Failed to delete " + f2 + " due to: " + str(ose))
        return target
    except:
        #traceback.print_exc(file=sys.stdout)
        log.exception("Exception whilst archiving files to directory")
        return None

if __name__ == "__main__":
    logging.basicConfig(filename="/var/log/pi-writer/typesetter.log", level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")
    log = logging.getLogger(__name__)
    configPath = os.path.join("/home/pi/pi-writer", "pi-writer.conf")
    config = ConfigParser.ConfigParser()
    config.read(configPath)
    publishDir = config.get("General", "publishDir")
    sentDir = config.get("General", "sentDir")
    
    typesetter = Typesetter()

    if typesetter.run():        
        # Email files
        log.info("Typesetter run successfully")
        
    # get all the files in the publish folder and email them
    files = []
    for (dirpath, dirnames, filenames) in os.walk(publishDir):
        for f in filenames:
            files.append(os.path.join(dirpath, f))
        break;
    
    log.info("There are " + str(len(files)) + " published files to email")
    if len(files) > 0:
        mailer = Mailer()
        
        if (mailer.send("Tests", "See Attackmented Text File(s)", files)):            
            # move the file to the sent directory
            archiveToDir(sentDir, files)
                
                

    
   # for file in files:
   #     typesetterThread = Typesetter(os.path.join(inputDir, file))
   #     typesetterThread.start()
   #     typesetterThread.join()
        
