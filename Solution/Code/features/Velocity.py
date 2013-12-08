'''
Created on 5-dec.-2013

@author: Koen
'''
import dataTransform.accproc as ac
import pandas as pd

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

def getVelocity(data):
    time = data.index
    
    velocity = dict()
    for v in ["Ax","Ay","Az"] :
        peaks = np.transpose(ac.detectPeaksGCDC(data, v))[0]
        velocity["V"+v[1:]] = get1DVel(time, data[v], peaks);
        
    return pd.DataFrame.from_dict(velocity)

import numpy as np
from tools.Tools import getFun, getCoVars

def getMeans(data):
    return getFun(data, np.mean, 'mean')

def getMins(data):
    return getFun(data, np.min, 'min')
    
def getMaxs(data):
    return getFun(data, np.max, 'max')

def getMedians(data):
    return getFun(data, np.median, 'median')



def getVelocityFeatures(data):
    data = getVelocity(data)
    features = getMeans(data)
    features.update(getMins(data))
    features.update(getMaxs(data))
    features.update(getMedians(data))
    features.update(getCoVars(data,'velocity'))
    
    return features
    
if __name__ == '__main__':
    import dataTransform.accproc as ac
    import dataTransform.Preprocessing as pp
    data = ac.readGCDCFormat("..\data\Runs\Example\enkel\DATA-001.csv")
    data = ac.preprocessGCDC(data)
    filtered = pp.filterRun3(data)
    
    velocity = getVelocity(filtered)
    print velocity
    features = getVelocityFeatures(filtered)
    print(features)
    
#     velocity.plot()
#     ppl.plot(t,filtered.Ax)
#     ppl.show()