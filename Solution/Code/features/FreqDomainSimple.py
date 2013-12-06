'''
Created on 5-dec.-2013

@author: jessa
'''
from scipy import fft
import pandas as pd

def toFreq(data) :
    data = data.apply(fft, axis=0)
    data = data[0:round(len(data.index)/2)]
    data = data.applymap(abs)
    data = data.apply(lambda ar: firstZero(ar),axis=0)
    index = pd.MultiIndex.from_arrays([range(len(data.index))])
    data.index = index
    return data

def firstZero(ar):
    ar[0]=0
    return ar

def getFun(data, func, prefix):
    features = data.apply(func, axis=0)
    features.rename(lambda x: prefix+ '.'+ x,inplace=True)
    return features.to_dict()


def getFirstN(data, n):
    features = dict()
    for i in range(n):
        features.update(getFun(data,lambda ar: ar[i],'F'+`i`))
        
    return features

def getNMainFreqs(data, n):
    data = data.apply(lambda ar: getLargestN(ar, n), axis=0)
    
    dic = dict()
    for label in data.index:
        dic.update(extractList(data.get(label),label,'MF'))
    
    return dic
        

def extractList(list, label, type):
    dic = dict()
    i=0
    for el in list:
        dic[type+`i`+'.'+label]=el
        i+=1
    return dic
    
    
    
def getLargestN(ser, n):
    ar = ser.values
    res = []
    
    for _ in range(n):
        imax = ar.argmax()
        ar[imax]=0
        res.append(imax)
     
    return res
    


def getSimpleFreqDomainFeatures(data):
    data = toFreq(data)
    data.Atotal.plot()
    features = getFirstN(data, 10)
    features.update(getNMainFreqs(data,5))
    
    return features