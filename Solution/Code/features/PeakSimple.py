'''
Created on 6-dec.-2013

@author: jessa
'''

def toPeaks(data) :
    data = data.apply(fft, axis=0)
    data = data[0:round(len(data.index)/2)]
    data = data.applymap(abs)
    data = data.apply(lambda ar: firstZero(ar),axis=0)
    index = pd.MultiIndex.from_arrays([range(len(data.index))])
    data.index = index
    return data