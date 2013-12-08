'''
Created on 5-dec.-2013

@author: Koen
'''
import dataTransform.accproc as ap
import matplotlib.pyplot as ppl
import pandas as pd
import numpy as np
from tools.Tools import getFun

def get1DVel(time,accSet,peaks):
    velocity = [(time[0],0)]
    accSet = ap.savitzky_golay(accSet, 11, 4)
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
        if (peaks and peaks[0] <= time[k+window_size] ):
            veli = 0
            peaks.pop(0)
        velocity.append((time[k+window_size],veli))
    velocity = zip(*velocity)
    velocity = pd.Series(velocity[1],velocity[0])
    print (velocity)
    return velocity

def getVelocity(data):
    time = data.index
    
    velocity = []
    axes = ["Ax","Ay","Az"]
    for v in axes :
        peaks = ac.detectPeaksGCDC(filtered, v)
        peaks = zip(*peaks)
#         ppl.plot(peaks[0],peaks[1])
        peaks = [x for x in peaks[0]]
    
        vel = get1DVel(time, data[v], peaks);
        velocity.append(vel)
        
    velocity = pd.concat(velocity, axis=1)
    velocity.columns = ["Vx","Vy","Vz"]
    return velocity

def getMeans(data):
    return getFun(data, np.mean, 'mean')

def getMins(data):
    return getFun(data, np.min, 'min')
    
def getMaxs(data):
    return getFun(data, np.max, 'max')

def getMedians(data):
    return getFun(data, np.median, 'median')

def getVelocityFeatures(data):
    features = getMeans(data)
    features.update(getMins(data))
    features.update(getMaxs(data))
    features.update(getMedians(data))
    
    return features
    
if __name__ == '__main__':
    import dataTransform.accproc as ac
    import dataTransform.Preprocessing as pp
    data = ac.readGCDCFormat("..\data\Runs\Example\enkel\DATA-001.csv")
    data = ac.preprocessGCDC(data)
    filtered = pp.filterRun3(data)
    
    velocity = getVelocity(filtered)
    print velocity
    velocity.plot()
#     ppl.plot(t,filtered.Ax)
    ppl.show()