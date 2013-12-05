'''
Created on 5-dec.-2013

@author: jessa
'''

import TimeDomainSimple as tds
import FreqDomainSimple as fds

def extract(data):
    
    features = fds.getSimpleFreqDomainFeatures(data)
    features.update(tds.getSimpleTimeDomainFeatures(data))
    return features