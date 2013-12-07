'''
Created on 5-dec.-2013

@author: jessa
'''

import TimeDomainSimple as tds
import FreqDomainSimple as fds
import PeakSimple as ps

def extract(data):
    
    features = fds.getSimpleFreqDomainFeatures(data)
    features.update(tds.getSimpleTimeDomainFeatures(data))
    #features.update(ps.getSimplePeakFeatures(data))
    return features