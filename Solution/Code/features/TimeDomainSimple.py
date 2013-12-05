'''
Created on 5-dec.-2013

@author: jessa
'''

import numpy as np

def getFun(data, func, prefix):
    features = data.apply(func, axis=0)
    features.rename(lambda x: prefix+ '.'+ x,inplace=True)
    return features.to_dict()

def getMeans(data):
    return getFun(data, np.mean, 'mean')

def getMins(data):
    return getFun(data, np.min, 'min')
    
def getMaxs(data):
    return getFun(data, np.max, 'max')

def getMedians(data):
    return getFun(data, np.median, 'median')


def getSimpleTimeDomainFeatures(data):
    features = getMeans(data)
    features.update(getMins(data))
    features.update(getMaxs(data))
    features.update(getMedians(data))
    
    return features