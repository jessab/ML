'''
Created on 29-nov.-2013

@author: Koen
'''

class Feature(object):
    '''
    classdocs
    '''


    def __init__(self, value):
        '''
        lol
        '''
        self.value=value
        
    def distance(self, other):
        return abs(self.value - other.value)
    
    def isLarger(self, other):
        return self.value > other.value
    
    def isLargerEqual(self, other):
        return self.value >= other.value
        