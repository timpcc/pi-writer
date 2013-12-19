'''
Created on 16 Dec 2013

@author: tim.crilly
'''
import re

class TextMangler():
    
    def __init__(self, replaceList):
        self.replaceList = replaceList

    def mangle(self, input):
        text = input
        for item in self.replaceList:
            print("using " + item["match"])
            while(re.search(item["match"], text, re.M) is not None):
                text = re.sub(item["match"], item["replace"], text, flags=re.MULTILINE)
                print(text)
        return text
