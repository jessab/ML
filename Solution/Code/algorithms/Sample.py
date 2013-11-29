'''
Created on 29-nov.-2013

@author: Koen
'''
from algorithms.Feature import Feature

class Sample(object):
    '''
    classdocs
    '''


    def __init__(self, filename):
        '''
        Constructor
        '''
        self.filename = filename
        self.max = Feature(max)
        self.min = Feature(min)
        
    def getMax(self):
        return self.max
    
    def getMin(self):
        return self.min
    
    def getAttributes(self):
        return [self.getMax(), self.getMin()]