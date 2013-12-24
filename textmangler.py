'''
Created on 16 Dec 2013

@author: tim.crilly
'''
import re
import logging

class TextMangler():
    
    def __init__(self, replaceList):
        self.logger = logging.getLogger(__name__)
        self.replaceList = replaceList

    def mangle(self, input):
        try:
            text = input
            for item in self.replaceList:
                while(re.search(item["match"], text, re.M) is not None):
                    text = re.sub(item["match"], item["replace"], text, flags=re.MULTILINE)
            return text
        except:
            self.logger.exception("Exception whilst mangling text")
            return None
