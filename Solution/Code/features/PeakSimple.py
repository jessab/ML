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

def maxDistanceBetweenPeaks(peaks):
    x=peaks[0]
    return max(x[1:-1]-x[0:-2]) 

def minDistanceBetweenPeaks(peaks):
    x=peaks[0]
    return min(x[1:-1]-x[0:-2]) 
    
def maxPeak(peaks):
    return max(peaks[1])

def minPeak(peaks):
    return min(filter(lambda x: x>0, peaks[1]))

def avPeak(peaks):
    return np.average(filter(lambda x: x>0, peaks[1]))    

def varPeak(peaks):
    return np.var(filter(lambda x: x>0, peaks[1]))




def getSimplePeakFeatures(data):
    peaks = toPeaks(data)
    features = applyFun(peaks,avDistanceBetweenPeaks, 'avDist')
    features.update(applyFun(peaks,varDistanceBetweenPeaks, 'varDist'))
    features.update(applyFun(peaks,maxDistanceBetweenPeaks, 'maxDist'))
    features.update(applyFun(peaks,minDistanceBetweenPeaks, 'minDist'))
    features.update(applyFun(peaks,maxPeak, 'maxPeak'))
    features.update(applyFun(peaks,minPeak, 'minPeak'))
    features.update(applyFun(peaks,avPeak,  'avPeak' ))
    features.update(applyFun(peaks,varPeak, 'varPeak'))
    return features
    
if __name__ == '__main__':
    import dataTransform.accproc as ac
    data = ac.readGCDCFormat("..\data\Runs\Example\enkel\DATA-001.csv")
    data = ac.preprocessGCDC(data)
    print(getSimplePeakFeatures(data))
