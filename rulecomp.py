
import ccm      
log=ccm.log(html=True)   
from ccm.lib.actr import *
from ccm.lib.actr.hdm import *


class RuleCompilation(ccm.Model):
    def runaction(self, motor, obj, goal):
        motorstr = ('self.motor.'+ motor + '(self,' + obj + ',' + 'location' + ',' + goal + ')')
        print (motorstr)
        #print(chunk) #is there some way to find a matching motor rule from a string? 
        return(motorstr)
        
    #requeststring puts remembered object in string for requesting appropriate action