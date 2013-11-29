'''
Created on 29-nov.-2013

@author: Koen
'''
from algorithms.Feature import Feature

class Sample(object):
    '''
    classdocs
    '''


    def __init__(self, testsubject, nb):
        '''
        Constructor
        '''
        self.testsubject = testsubject
        self.max = Feature(maxi)
        self.min = Feature(mini)
        self.classification = Classification(trained, terrain)
        
    def getMax(self):
        return self.max
    
    def getMin(self):
        return self.min
    
    def getAttributes(self):
        return [self.getMax(), self.getMin()]
    
    def isTrained(self):
        return self.classification.trained
    
    def getTerrain(self):
        return self.classification.terrain
    
    def getClassification(self):
        return self.classification