'''
Created on 6-dec.-2013

@author: jessa
'''
import numpy as np
import pylab

try:
    from dataTransform.accproc import detectPeaksGCDC
except:
    print('import failed')

def peakTupToStr(tup):
    detType,smoothType,smoothCor = tup
    
    if smoothType is None:
        return detType+'_notSmooth'
    else:
        name = detType+'_'+smoothType
    if smoothCor :
        name += '_cor'
    else :
        name += '_ncor'
        
    return name
        
def genPeaks(data,tup):
    
    detType,smoothType,smoothCor = tup
    if smoothType is None :
        val = detectPeaksGCDC(data,detection={'type':detType})
        val = np.transpose(val)
    else:
        val = np.transpose(detectPeaksGCDC(data,detection={'type':detType}, smooth={'type':smoothType, 'correct':smoothCor}))
    if len(val[0])<10:
        val=None
    return val

def toPeaks(data, peakTups) :
    #TODO play with windows and stuff
    
    peaks = dict()
    
    for tup in peakTups:
        if len(tup)==2:
            detType,smoothType = tup
            tup = (detType,smoothType,False)
            
        name = peakTupToStr(tup)
    
        try:
            peaks[name]=genPeaks(data,tup)
        except Exception as ex:
            print(ex)
            print(name)
            peaks[name]=None
            continue
        
    return peaks

def applyFun(dic, fun, postfix):
    res = dict({k + "." + postfix: fun(dic[k]) for k in dic.keys() if dic[k] is not None})
    res.update(dict({k+"."+postfix:None for k in dic.keys() if dic[k] is None}))
    return res
    
def avDist(peaks):
    x=peaks[0]
    return np.average(x[1:]-x[:-1])    
    
def varDist(peaks):
    x=peaks[0]
    return np.var(x[1:]-x[:-1]) 

def maxDist(peaks):
    x=peaks[0]
    return max(x[1:]-x[:-1]) 

def minDist(peaks):
    x=peaks[0]
    return min(x[1:]-x[:-1]) 

def medianDist(peaks):
    x=peaks[0]
    return np.median(x[1:]-x[:-1])
    
def maxPeak(peaks):
    return max(peaks[1])

def minPeak(peaks):
    return min(peaks[1])

def avPeak(peaks):
    return np.average(peaks[1])    

def varPeak(peaks):
    return np.var(peaks[1])

def medianPeak(peaks):
    return np.median(peaks[1])


def posFeatures():
    return {
        'avDist' : avDist,
        'varDist': varDist,
        'minDist': minDist,
        'maxDist': maxDist,
        'medianDist': medianDist,
        'avPeak' : avPeak,
        'varPeak': varPeak,
        'minPeak': minPeak,
        'maxPeak': maxPeak,
        'medianPeak': medianPeak
    }
    
def posPeaks():
    withoutSmooth = [(dt,None) for dt in ['simple','cwt']]
    withSmooth = [(dt,st,sc) for dt in ['simple','cwt'] for st in ['hilbert','sg','butter'] for sc in [True,False]]
    return withoutSmooth+withSmooth

def getSimplePeakFeatures(data, requiredFeatures=None):
    generatedFeatures = {'cols':posPeaks(), 'features':posFeatures().keys()}
    if requiredFeatures is None:
        requiredFeatures = generatedFeatures
    generatedFeatures.update(requiredFeatures)
    
    peaks = toPeaks(data,generatedFeatures['cols'])
    
    features = dict()
    
    for f in generatedFeatures['features'] :
        features.update(applyFun(peaks,posFeatures()[f],f))

    return features
    
if __name__ == '__main__':
    import dataTransform.accproc as ac
    import dataTransform.Preprocessing as pp
    for i in range(9):
        nb = int(i+1)
        if nb== 4:
            data = ac.readGCDCFormat("..\..\Runs\Tina\enkel\DATA-00" + `nb` + ".csv")
            data = ac.preprocessGCDC(data)
            filtered = pp.filterRun3(data,False)

            print(getSimplePeakFeatures(data))
