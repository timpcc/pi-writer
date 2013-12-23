'''
Created on 13 Dec 2013

@author: tim.crilly
'''
import re
import ConfigParser
import os
import json
import logging
import sys
import traceback;

class CommandRunner():
    
    def __init__(self):
        try:
            self.logging.basicConfig(filename="pi-writer.log", level=logging.DEBUG)
            self.logger = logging.getLogger(__name__)
            configPath = os.path.join("/home/pi", "pi-writer", "pi-writer.conf")
            self.config = ConfigParser.ConfigParser()
            self.config.read(configPath)
        except:
            if self.logger is not None:
                self.logger.exception("Exception whilst setting up command runner")
            else:
                print("Exception whilst setting up command runner")
                traceback.print_exc(file=sys.stdout)

    def run(self, data):
        try:
            text = data
            self.logger.debug("Parsed command: " + text)
            # get id - get first line
            m_id = re.match(r"(?P<id>[A-Za-z0-9\._]+)", text)
            if m_id is not None:
                id = m_id.group("id")
                
            self.logger.debug("Using ID: " + id)
                    
            if id is not None:
                # get the config for this id
                command = self.config.get("Commands", id);
                command_obj = json.loads(command)
                if command_obj is not None:
                    m = re.match(command_obj["pattern"], text)
                    
                    cmd = command_obj["command"]
                    self.logger.debug("Command: " + cmd)
                    if (m.group is not None):
                        for g in command_obj["groups"]:
                            cmd = cmd.replace("%"+g+"%", m.group(g))
                    self.logger.debug(cmd)
                    status = os.system(cmd)        
                    self.logger.debug("ExitCode: " + str(status))
                    if status == 0:
                        return True
                    else: 
                        return False
            else:
                self.logger.debug("Cannot find id in command")
                return False
                
        except Exception as e:
            self.logger.exception("Exception whilst executing command")
            #raise e
            return False
           
#    def parseCommandString(self, text):
#        for item in self.replaceList:
#            text = re.sub(item["match"], item["replace"], text)
#        return text
            