'''
Created on 5-dec.-2013

@author: jessa
''' 

import TimeDomainSimple as tds
import FreqDomainSimple as fds
import PeakSimple as ps
import Velocity as vs


def checkRequiredFeatures(requiredFeatures,generatedFeatures):
    if requiredFeatures is None:
        requiredFeatures = generatedFeatures
    generatedFeatures.update(requiredFeatures)
    
    return generatedFeatures

def extractBodyPart(data, bodyPart, requiredFeatures=None):
    requiredFeatures=checkRequiredFeatures(requiredFeatures,{'time':None, 'freq': None, 'peak':None, 'vel':None})
    
    
    features = dict()
    features.update(fds.getSimpleFreqDomainFeatures(data,requiredFeatures['freq']))
    features.update(tds.getSimpleTimeDomainFeatures(data,requiredFeatures['time']))
    features.update(ps.getSimplePeakFeatures(data,requiredFeatures['peak']))
    features.update(vs.getVelocityFeatures(data,requiredFeatures['vel']))
    
    features = dict((bodyPart+'.'+key,features[key]) for key in features.keys())
    
    return features

def extract(ankleData,hipData,requiredFeatures=None):
    requiredFeatures = checkRequiredFeatures(requiredFeatures,{'ankle':None,'hip':None})
    
    features = dict()
    
    features.update(extractBodyPart(ankleData, 'ankle', requiredFeatures['ankle']))
    features.update(extractBodyPart(hipData, 'hip', requiredFeatures['hip']))
    
    return features

def getAllFeatures():
    part = {
        'time': {
                 'cols': tds.posCols(),
                 'features': tds.posFeatures().keys()
                 }, 
        'freq': {
                 'cols': fds.posCols(),
                 'features': fds.posFeatures().keys()
                 },
        'vel' : {
                 'cols': vs.posCols(),
                 'features': vs.posFeatures().keys()
                 },
        'peak': {
                 'cols': ps.posPeaks(),
                 'features': ps.posFeatures().keys()
                 }
        }
    
    return {
        'ankle':part,
        'hip':part   
        }