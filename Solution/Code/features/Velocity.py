'''
Created on 5-dec.-2013

@author: Koen
'''
import dataTransform.accproc as ac
import pandas as pd
import numpy as np
from tools.Tools import getFun, getCoVars

def get1DVel(time,accSet,peaks):
    velocity = [(time[0],0)]
    accSet = ac.savitzky_golay(accSet, 11, 4)
    window_size = 32
    nbSamples = len(time)/window_size
    for i in range(nbSamples-1):
        k = window_size*i
#         if (t == peaks[0]):
#             velocity.append(0)
#             peaks.pop(0)
#         else:
        dt = time[k+window_size] - time[k]
        da = (sum(accSet[k:k+window_size])-sum(accSet[k+window_size:k+2*window_size]))/window_size
#         if (abs(da) < 0.010):
#             da = 0
        veli = (velocity[-1][1] + dt*da/2)
        if (len(peaks)>0 and peaks[0] <= time[k+window_size] ):
            veli = 0
            peaks = peaks[:-1]
        velocity.append((time[k+window_size],veli))
    velocity = zip(*velocity)
    velocity = pd.Series(velocity[1],velocity[0])
#     print (velocity)
    return velocity

def getVelocity(data,cols):
    time = data.index
    
    velocity = dict()
    for v in cols:
        orgCol="A"+v[1:]
        peaks = np.transpose(ac.detectPeaksGCDC(data, orgCol,smooth={'type':'sg'}))[0]
        velocity[v] = get1DVel(time, data[orgCol], peaks);
        
    return pd.DataFrame.from_dict(velocity)

def posFeatures():
    return {
        'av' : (np.average,True),
        'covar': (getCoVars,False),
        'min': (np.min,True),
        'max': (np.max,True),
        'median': (np.median,True)
    }
    
def posCols():
    return ['Vx','Vy','Vz']

def checkRequiredFeatures(requiredFeatures):
    generatedFeatures = {'cols':posCols(), 'features':posFeatures().keys()}
    if requiredFeatures is None:
        requiredFeatures = generatedFeatures
    generatedFeatures.update(requiredFeatures)
    generatedFeatures['cols']= [col for col in generatedFeatures['cols'] if col in posCols()]
    generatedFeatures['features']= [f for f in generatedFeatures['features'] if f in posFeatures().keys()]
    
    return generatedFeatures
    
    

def getVelocityFeatures(data, requiredFeatures=None):
    requiredFeatures = checkRequiredFeatures(requiredFeatures)
    data = getVelocity(data,requiredFeatures['cols'])
    
    features = dict()
    for f in requiredFeatures['features']:
        fun,useGetFun = posFeatures()[f]
        if useGetFun:
            ff = getFun(data,fun,f)
        else :
            ff = fun(data,f)
        features.update(ff)
        
    return features

    
if __name__ == '__main__':
    import dataTransform.Preprocessing as pp
    data = ac.readGCDCFormat("..\data\Runs\Example\enkel\DATA-001.csv")
    data = ac.preprocessGCDC(data)
    filtered = pp.filterRun3(data)
    
    velocity = getVelocity(filtered,['Vx','Vz'])
    print velocity
    features = getVelocityFeatures(filtered,{'cols':['Vx'],'features':['covar','av']})
    print(features)
    
#     velocity.plot()
#     ppl.plot(t,filtered.Ax)
#     ppl.show()
