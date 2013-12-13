'''
Created on 5-dec.-2013

@author: jessa
'''
from scipy import fft

import pandas as pd
from tools.Tools import getFun, getCoVars


def toFreq(data):
    data = data.apply(fft, axis=0)
    data = data[0:round(len(data.index) / 2)]
    data = data.applymap(abs)
    data = data.apply(lambda ar: firstZero(ar), axis=0)
    index = pd.MultiIndex.from_arrays([range(len(data.index))])
    data.index = index
    return data


def firstZero(ar):
    ar[0] = 0
    return ar


def getFirstN(data, name, n):
    features = dict()
    for i in range(n):
        features.update(getFun(data, lambda ar: ar[i], name + `i`))

    return features


def getNMainFreqs(data, name, n):
    data = data.apply(lambda ar: getLargestN(ar, n), axis=0)

    dic = dict()
    for label in data.index:
        dic.update(extractList(data.get(label), label, name))

    return dic


def extractList(lijst, label, typ):
    dic = dict()
    i = 0
    for el in lijst:
        dic[typ + `i` + '.' + label] = el
        i += 1
    return dic


def getLargestN(ser, n):
    ar = ser.values
    res = []

    for _ in range(n):
        imax = ar.argmax()
        ar[imax] = 0
        res.append(imax)

    return res


def posFeatures():
    return {
        'MF': lambda data, name: getNMainFreqs(data, name, 10),
        'F': lambda data, name: getFirstN(data, name, 10),
        'fcovar': getCoVars
    }


def posCols():
    return ['Ax', 'Ay', 'Az', 'Atotal']


def checkRequiredFeatures(requiredFeatures):
    generatedFeatures = {'cols': posCols(),
                         'features': posFeatures().keys()}
    if requiredFeatures is None:
        requiredFeatures = generatedFeatures
    generatedFeatures.update(requiredFeatures)
    generatedFeatures['cols'] = [col for col in generatedFeatures['cols']
                                 if col in posCols()]
    generatedFeatures['features'] = [f for f in generatedFeatures['features']
                                     if f in posFeatures().keys()]

    return generatedFeatures


def getSimpleFreqDomainFeatures(data, requiredFeatures=None):
    requiredFeatures = checkRequiredFeatures(requiredFeatures)

    data = toFreq(data[requiredFeatures['cols']])

    features = dict()

    for f in requiredFeatures['features']:
        features.update(posFeatures()[f](data, f))

    return features

if __name__ == '__main__':
    import dataTransform.accproc as ac
    import dataTransform.Preprocessing as pp
    for i in range(9):
        nb = int(i + 1)
        if nb == 4:
            data = ac.readGCDCFormat("..\data\Runs\Tina\enkel\DATA-00" +
                                     `nb` + ".csv")
            data = ac.preprocessGCDC(data)
            filtered = pp.filterRun3(data)
            print(getSimpleFreqDomainFeatures(data, None))
