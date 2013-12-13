'''
Created on 13 Dec 2013

@author: tim.crilly
'''
import re
import ConfigParser

class CommandRunner():
    
    def __init__(self):
        configPath = os.path.join(os.environ.get("XDG_CONFIG_HOME"), "pi-writer", "pi-writer.conf")
        self.config = ConfigParser.ConfigParser()
        self.config.read(configPath)
        #self.workDir = self.config.get("Commands", "workDir")
        

    def run(self, data):
        try:
            # get id - get first line
            m_id = re.match(r"(?P<id>[A-Za-z\t .]+)", data)
            if m_id is not None:
                id = m_id.group("id")
                
            print("Using ID: " + id)
            
            if id is not None:
                # get the config for this id
                command = self.config.get("Commands", id);
                
                if command is not None:
                    m = re.match(command["pattern"], data)
                    cmd = command["command"]
                    print("Command: " + cmd)
                    for g in command["groups"]:
                        cmd = cmd.replace("%"+g+"%", m.group(g))
                        print(cmd)
                    return True
            else:
                print("Cannot find id in command")
                return False
                
        except Exception:
            return False
             
            