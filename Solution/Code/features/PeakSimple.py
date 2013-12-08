'''
Created on 6-dec.-2013

@author: jessa
'''
import numpy as np
from dataTransform.accproc import detectPeaksGCDC

def toPeaks(data) :
    #TODO play with windows and stuff
    
    def genDictEntry(detType, smoothType, smoothCor):
        
        if smoothType is None:
            key = detType+'_notSmooth'
        else:
            key = detType+'_'+smoothType
        if smoothCor :
            key += '_cor'
        else :
            key += '_ncor'
        try:
            if smoothType is None :
                val= np.transpose(detectPeaksGCDC(data,detection={'type':detType}, smooth=None))
            else:
                val = np.transpose(detectPeaksGCDC(data,detection={'type':detType}, smooth={'type':smoothType, 'correct':smoothCor}))
            if len(val[0])<10:
                val=None
            return {key:val}
        except:
            return {key:None}
    
    peaks = genDictEntry('simple', None, None)
    peaks.update(genDictEntry('simple','hilbert',True))
    peaks.update(genDictEntry('simple','hilbert',False))
    peaks.update(genDictEntry('simple','sg',True))
    peaks.update(genDictEntry('simple','sg',False))
    peaks.update(genDictEntry('simple','butter',True))
    peaks.update(genDictEntry('simple','butter',False))
    peaks.update(genDictEntry('cwt',None,None))
    peaks.update(genDictEntry('cwt','hilbert',True))
    peaks.update(genDictEntry('cwt','hilbert',False))
    peaks.update(genDictEntry('cwt','sg',True))
    peaks.update(genDictEntry('cwt','sg',False))
    peaks.update(genDictEntry('cwt','butter',True))
    peaks.update(genDictEntry('cwt','butter',False))
    return peaks

def applyFun(dic, fun, postfix):
    res = dict({k + "." + postfix: fun(dic[k]) for k in dic.keys() if dic[k] is not None})
    res.update(dict({k+"."+postfix:None for k in dic.keys() if dic[k] is None}))
    return res
    
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
    import dataTransform.Preprocessing as pp
    for i in range(9):
        nb = int(i+1)
        if nb== 4:
            data = ac.readGCDCFormat("..\data\Runs\Tina\enkel\DATA-00" + `nb` + ".csv")
            data = ac.preprocessGCDC(data)
            filtered = pp.filterRun3(data)
            print(getSimplePeakFeatures(data))
