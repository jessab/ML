'''
Created on 5-dec.-2013

@author: jessa
''' 

import TimeDomainSimple as tds
import FreqDomainSimple as fds
import PeakSimple as ps
import Velocity as vs

def extract(data):
    
    features = fds.getSimpleFreqDomainFeatures(data)
    features.update(tds.getSimpleTimeDomainFeatures(data))
    features.update(ps.getSimplePeakFeatures(data))
    features.update(vs.getVelocityFeatures(data))
    
    return features