'''
Created on 13 Dec 2013

@author: tim.crilly
'''
import re
import ConfigParser
import os
import json

class CommandRunner():
    
    def __init__(self):
        configPath = os.path.join(os.environ.get("XDG_CONFIG_HOME"), "pi-writer", "pi-writer.conf")
        self.config = ConfigParser.ConfigParser()
        self.config.read(configPath)
        #self.workDir = self.config.get("Commands", "workDir")
        data = self.config.get("CommandParser", "patterns")
        self.replaceList = json.loads(data)

    def run(self, data):
        #try:
        text = self.parseCommandString(data)
        print("Parsed command: " + text)
        # get id - get first line
        m_id = re.match(r"(?P<id>[A-Za-z0-9\._]+)", text)
        if m_id is not None:
            id = m_id.group("id")
            
        print("Using ID: " + id)
                
        if id is not None:
            # get the config for this id
            command = self.config.get("Commands", id);
            command_obj = json.loads(command)
            if command_obj is not None:
                m = re.match(command_obj["pattern"], text)
                
                cmd = command_obj["command"]
                print("Command: " + cmd)
                if (m.group is not None):
                    for g in command_obj["groups"]:
                        cmd = cmd.replace("%"+g+"%", m.group(g))
                print(cmd)
                status = os.system(cmd)        
                print("ExitCode: " + str(status))
                if status == 0:
                    return True
                else: 
                    return False
        else:
            print("Cannot find id in command")
            return False
                
        #except Exception as e:
        #    print("Exception: " + str(e))
        #    raise e
            #return False
           
    def parseCommandString(self, text):
        for item in self.replaceList:
            text = re.sub(item["match"], item["replace"], text)
        return text
            