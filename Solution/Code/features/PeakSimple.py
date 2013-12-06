'''
Created on 6-dec.-2013

@author: jessa
'''
import numpy as np
from dataTransform.accproc import detectPeaksGCDC

def toPeaks(data) :
    #TODO Add more peaks
    return {'default':np.transpose(detectPeaksGCDC(data,columnname='Ax'))}

def applyFun(dic, fun, postfix):
    return dict({k + "." + postfix: fun(dic[k]) for k in dic.keys()})
    
def avDistanceBetweenPeaks(peaks):
    x=peaks[0]
    return np.average(x[1:-1]-x[0:-2])    
    
def varDistanceBetweenPeaks(peaks):
    x=peaks[0]
    return np.var(x[1:-1]-x[0:-2]) 

def maxPosPeak(peaks):
    return max(peaks[1])

def maxNegPeak(peaks):
    return min(peaks[1])

def minPosPeak(peaks):
    return min(filter(lambda x: x>0, peaks[1]))

def minNegPeak(peaks):
    return max(filter(lambda x: x<0, peaks[1]))

def maxAbsPeak(peaks):
    return max(map(np.abs,peaks))

def minAbsPeak(peaks):
    return min(map(np.abs,peaks))

def avPosPeak(peaks):
    return np.average(filter(lambda x: x>0, peaks[1]))
    
def avNegPeak(peaks):
    return np.average(filter(lambda x: x<0, peaks[1]))

def avAbsPeak(peaks):
    return np.average(map(np.abs,peaks))

def varPosPeak(peaks):
    return np.var(filter(lambda x: x>0, peaks[1]))
    
def varNegPeak(peaks):
    return np.var(filter(lambda x: x<0, peaks[1]))

def varAbsPeak(peaks):
    return np.var(map(np.abs,peaks))



def getSimplePeakFeatures(data):
    peaks = toPeaks(data)
    features = applyFun(peaks,avDistanceBetweenPeaks, 'avDist')
    features.update(applyFun(peaks,varDistanceBetweenPeaks, 'varDist'))
    features.update(applyFun(peaks,maxPosPeak, 'maxPosPeak'))
#     features.update(applyFun(peaks,maxNegPeak, 'maxNegPeak'))
    features.update(applyFun(peaks,minPosPeak, 'minPosPeak'))
#     features.update(applyFun(peaks,minNegPeak, 'minNegPeak'))
#    features.update(applyFun(peaks,maxAbsPeak, 'maxAbsPeak'))
#    features.update(applyFun(peaks,minAbsPeak, 'minAbsPeak'))
    features.update(applyFun(peaks,avPosPeak,  'avPosPeak' ))
#     features.update(applyFun(peaks,avNegPeak,  'avNegPeak' ))
#    features.update(applyFun(peaks,avAbsPeak,  'avAbsPeak' ))
    features.update(applyFun(peaks,varPosPeak, 'varPosPeak'))
#     features.update(applyFun(peaks,varNegPeak, 'varNegPeak'))
#    features.update(applyFun(peaks,varAbsPeak, 'varAbsPeak'))
    return features
    
if __name__ == '__main__':
    import dataTransform.accproc as ac
    data = ac.readGCDCFormat("..\data\Runs\Example\enkel\DATA-001.csv")
    data = ac.preprocessGCDC(data)
    print(getSimplePeakFeatures(data))
