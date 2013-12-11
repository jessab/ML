'''
Created on 10-dec.-2013

@author: jessa
'''

import TimeDomainSimple as tds
import Velocity as vel
import FreqDomainSimple as fds
import PeakSimple as ps

def findBodyPart(bodyPart):
    if 'anckle' in bodyPart:
        return 'anckle'
    if 'hip' in bodyPart:
        return 'hip'

def findCategory(el,feat):
    if 'A' in el : #Time or Freq
        if feat in tds.posFeatures().keys():
            return 'time'
        else:
            return 'freq'
    elif 'V' in el: #Velocity
        return 'vel'
    return 'peak'

def findCols(cat, el):
    if cat=='time':
        return [col for col in tds.posCols() if col in el]
    if cat=='freq':
        return [col for col in fds.posCols() if col in el]
    if cat=='vel':
        return [col for col in vel.posCols() if col in el]
    if cat=='peak':
        parts = el.split('_')
        if len(parts)==2:
            return [(parts[0],None)]
        if len(parts)==3:
            return [(parts[0],parts[1],parts[2]=='cor')]
        return []
    
def findFeature(cat,feat):
    if cat =='time':
        return [f for f in tds.posFeatures().keys() if f in feat]
    if cat == 'freq':
        return [f for f in fds.posFeatures().keys() if f in feat]
    if cat == 'vel':
        return [f for f in vel.posFeatures().keys() if f in feat]
    if cat == 'peak':
        return [f for f in  ps.posFeatures().keys() if f in feat]
        
         
def addFeatureToDict(dic,f):
    [bodyPart, el,feat] = f.split('.')
    
    bodyPart = findBodyPart(bodyPart)
    if bodyPart is None:
        return dic
    
    cat = findCategory(el, feat)
    cols = findCols(cat,el)
    features = findFeature(cat,feat)
    
    dic[bodyPart][cat]['cols']+=[c for c in cols if c not in dic[bodyPart][cat]['cols']]
    dic[bodyPart][cat]['features']+=[f for f in features if f not in dic[bodyPart][cat]['features']]
    
    return dic

def basicCatDict():
    return {
        'cols':[],
        'features':[]
        }

def basicBodyDict():
    return {
        'time':basicCatDict(),
        'freq':basicCatDict(),
        'vel':basicCatDict(),
        'peak':basicCatDict()
        }
def basicDict():
    return {
        'anckle':basicBodyDict(),
        'hip': basicBodyDict()
        }

def featuresToRequiredDict(requiredFeatures):
    dic = basicDict()
    
    for f in requiredFeatures:
        dic = addFeatureToDict(dic, f)
        
    return dic
         
    

if __name__ == '__main__':
    features = ['hip.Ax.min', 'anckle.AyAz.fcovar','hip.Vx.av','anckle.simple_nosmooth.maxDist','hip.cwt_butter_ncor.avPeak','anckle.cwt_butter_cor.maxDist', 'head.fout.ief']
    print(featuresToRequiredDict(features))