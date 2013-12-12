'''
Created on 29-nov.-2013

@author: jessa
'''

import matplotlib.pyplot as plt
import dataTransform.accproc as ac
import features.FeatureExtraction as fa
from IPython.core.display import display
import pylab
import math
from scipy import fft, ifft
import pandas as pd
import app.featuresMain as fm
import numpy as np
from tools.Tools import getDictArray
from cgi import maxlen

def accproctest() :
    data = ac.readGCDCFormat("..\data\Runs\Example\enkel\DATA-001.csv")
    print("Before preprocessing")
    print(data[0:10])
    data = ac.preprocessGCDC(data)
    print("After preprocessing")
    print(data[0:10])
    data.plot()
    dataslice = data[(100 < data.index) & (data.index < 105)]
    plt.figure(figsize=plt.figaspect(0.33))
    dataslice.plot()

    plt.figure(figsize=plt.figaspect(0.33))
    plt.title("Ax signal")
    dataslice.Ax.plot()

    plt.figure(figsize=plt.figaspect(0.33))
    plt.title("Atotal signal")
    dataslice.Atotal.plot()
    
    calslice = data[(20 < data.index) & (data.index < 35)]

    plt.figure(figsize=plt.figaspect(0.33))
    calslice.plot()
    
    plt.figure(figsize=plt.figaspect(0.33))
    plt.title("Ax with Envelope+Butterworth filter (5Hz)")
    _max = ac.detectPeaksGCDC(dataslice, columnname="Ax",
                                     detection={'delta': 1.0},
                                     smooth={'type': 'hilbert,butter',
                                             'fcol': 5,
                                             'correct': True},
                                     plot=True, verbose=True)

    plt.figure(figsize=plt.figaspect(0.33))
    plt.title("Az with Hilbert+Butter filter (enveloppe+lowpass@10Hz) and correcting")
    _ = ac.detectPeaksGCDC(dataslice, columnname="Az",
                            detection={'lookahead':40, 'delta':0.4},
                            smooth={'type':'hilbert,butter',
                                    'fcol':10,
                                    'window':31, 'correct':True},
                            plot=True, verbose=True)

    pylab.show()

    
def sliding_window(ar, width, freq):
    nbOfWindows = int(math.floor((len(ar)-width)/freq))
    
    res = []
    
    for i in range(nbOfWindows):
        start = i*freq
        end   = start+width
        res.append([ar[start:end]])
    
    return res

def getFeatures(path,name,nb) :
    from features.PeakSimple import applyFun, toPeaks, varDistanceBetweenPeaks
    data = fm.getData(path,name,nb)
    print(data  )
    if data is None:
        print("NONE")
        return None
    print("SOME")
    peaks = toPeaks(data)
    print(peaks)
    features = applyFun(peaks,varDistanceBetweenPeaks, 'varDist')
    return features

if __name__ == '__main__':
    import pickle
    alle = {'ankle': {'freq': {'cols': ['Ax', 'Ay', 'Az', 'Atotal'], 'features': ['fcovar', 'MF', 'F']}, 'vel': {'cols': ['Vx', 'Vy', 'Vz'], 'features': ['covar', 'max', 'min', 'median', 'av']}, 'peak': {'cols': [('simple', None), ('cwt', None), ('simple', 'hilbert', True), ('simple', 'hilbert', False), ('simple', 'sg', True), ('simple', 'sg', False), ('simple', 'butter', True), ('simple', 'butter', False), ('cwt', 'hilbert', True), ('cwt', 'hilbert', False), ('cwt', 'sg', True), ('cwt', 'sg', False), ('cwt', 'butter', True), ('cwt', 'butter', False)], 'features': ['varDist', 'maxDist', 'avDist', 'varPeak', 'avPeak', 'minDist', 'maxPeak', 'minPeak']}, 'time': {'cols': ['Ax', 'Ay', 'Az', 'Atotal'], 'features': ['covar', 'max', 'min', 'median', 'av']}}, 'hip': {'freq': {'cols': ['Ax', 'Ay', 'Az', 'Atotal'], 'features': ['fcovar', 'MF', 'F']}, 'vel': {'cols': ['Vx', 'Vy', 'Vz'], 'features': ['covar', 'max', 'min', 'median', 'av']}, 'peak': {'cols': [('simple', None), ('cwt', None), ('simple', 'hilbert', True), ('simple', 'hilbert', False), ('simple', 'sg', True), ('simple', 'sg', False), ('simple', 'butter', True), ('simple', 'butter', False), ('cwt', 'hilbert', True), ('cwt', 'hilbert', False), ('cwt', 'sg', True), ('cwt', 'sg', False), ('cwt', 'butter', True), ('cwt', 'butter', False)], 'features': ['varDist', 'maxDist', 'avDist', 'varPeak', 'avPeak', 'minDist', 'maxPeak', 'minPeak']}, 'time': {'cols': ['Ax', 'Ay', 'Az', 'Atotal'], 'features': ['covar', 'max', 'min', 'median', 'av']}}}
    print(alle)
    print(type(alle))
    path = "..\data\\"
    name = ".._.._Runs_"
    f = file(path+name, "w")
    pickle.dump(alle, f)