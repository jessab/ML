'''
Created on 10-dec.-2013

@author: jessa
'''
from ast import literal_eval
import pickle

import dataTransform.Preprocessing as pp
import dataTransform.accproc as ac
import features.FeatureExtraction as fa
import pandas as pd
from tools.nestedDictTools import diff, union, isEmpty, colsFirstFeaturesSecond

import os


def getDataPath():
    posPaths = ["data\\", "..\data\\", "..\..\data"]
    for path in posPaths:
        if os.path.isdir(path):
            return path
    raise Exception("Path to Data info does not exist")


def getName(path):
    return path.replace("//", "_").replace("/", '_').replace("\\", '_')


def loadExistingData(name):
    return pd.read_csv(getDataPath() + name + ".csv", sep=";", index_col=0)


def getExistingFeatures(name):
    pfile = file(getDataPath() + name, "r")
    # look up existing features
    return pickle.load(pfile)


def getFeatures(path, name, nb, required, existing, existingVals):
    def getRawData(path, name, nb, hip):
        def getDir(path, subject, bodyPart, nb):
            return (path + subject + "\\" + bodyPart + "\\" +
                    "DATA-00" + str(int(nb)) + ".csv")
        if hip:
            bodyPart = 'heup'
        else:
            bodyPart = 'enkel'
        datadir = getDir(path, name, bodyPart, nb)
        try:
            data = ac.readGCDCFormat(datadir)
        except:
            return None
        return ac.preprocessGCDC(data)

    def getRunningPart(data, hip):
        try:
            return pp.filterRun3(data, hip)
        except:
            return None

    def obtainFeatures(ankleData, hipData, features):
        try:
            return fa.extract(ankleData, hipData, features)
        except:
            return None

    def getDataForOneBodyPart(path, name, nb, hip):
        data = getRawData(path, name, nb, hip)
        data = getRunningPart(data, hip)
        return data

    ankleData = getDataForOneBodyPart(path, name, nb, False)
    hipData = getDataForOneBodyPart(path, name, nb, True)

    if existing is None:
        f = obtainFeatures(ankleData, hipData, required)
        if f is None:
            print('no features')
            return None
        return str(f)

    missingFeatures = diff(required, existing)

    # obtain features for existing cols and new features
    newFeaturesForOldCols = colsFirstFeaturesSecond(existing, missingFeatures)
    f1 = obtainFeatures(ankleData, hipData, newFeaturesForOldCols)

    # obtain features for new cols and all features
    featuresForNewCols = colsFirstFeaturesSecond(missingFeatures,
                                            union(missingFeatures, existing))
    f2 = obtainFeatures(ankleData, hipData, featuresForNewCols)

    if f1 is not None:
        f = f1
        if f2 is not None:
            f.update(f2)
    elif f2 is not None:
        f = f2
    else:
        print('no features')
        return None

    if existingVals is not None:
        existingVals = literal_eval(existingVals)
        existingVals.update(f)
        f = existingVals
    return str(f)


def updateFeatures(data, path, features, existingFeatures=None):
    if existingFeatures is None:
        data['Features'] = data.apply(lambda row:
                                      getFeatures(path, row['Name'], row['Nb'],
                                    features, None, None), axis=1)
    else:
        data['Features'] = data.apply(lambda row:
                                      getFeatures(path, row['Name'], row['Nb'],
                                    features, existingFeatures,
                                    row['Features']), axis=1)
    return data


def loadNewData(path):
    filename = path + "metadata.csv"
    df = pd.io.parsers.read_csv(filename,
                      names=["Name", "Nb", "Trained", "Surface", "Sec"],
                      skiprows=2,
                      sep=";")
    df = df.dropna(thresh=3)

    return df


def storeData(data, name):
    data.to_csv(getDataPath() + name + ".csv", sep=";")


def storePickle(features, name):
    f = file(getDataPath() + name, "w")
    pickle.dump(features, f)


def cleanData(data):

    def questionMarkToNaN(val):
        if type(val) == float:
            return val
        if "?" in val:
            return float('NaN')
        else:
            return float(val.strip())

    def ynToTF(val):
        if type(val) == bool:
            return val
        if "y" in val:
            return True
        else:
            return False

    data = data[data.apply(lambda x: x['Features'] is not None, axis=1)]
    data['Sec'] = data.apply(lambda x: questionMarkToNaN(x['Sec']), axis=1)
    data['Trained'] = data.apply(lambda x: ynToTF(x['Trained']), axis=1)
    data['Nb'] = data['Nb'].astype(int)
    index = pd.MultiIndex.from_arrays([range(len(data.index))])
    data.index = index
    return data


def getDataExisting(path, requiredFeatures):
    name = getName(path)
    data = loadExistingData(name)
    existingFeatures = getExistingFeatures(name)
#     mFeatures =  diff(requiredFeatures,existingFeatures)
    if isEmpty(diff(requiredFeatures, existingFeatures)):
        return data
    data = updateFeatures(data, path, requiredFeatures, existingFeatures)
    data = cleanData(data)
    storeData(data, name)
    storePickle(union(requiredFeatures, existingFeatures), name)
    return data


def getDataNotExisting(path, requiredFeatures):
    name = getName(path)
    data = loadNewData(path)
    data = updateFeatures(data, path, requiredFeatures)
    data = cleanData(data)
    storeData(data, name)
    storePickle(requiredFeatures, name)
    return data


def getData(path, requiredFeatures, useExisting):
    if requiredFeatures is None:
        requiredFeatures = fa.getAllFeatures()
    if useExisting:
        try:
            return getDataExisting(path, requiredFeatures)
        except:
            return getDataNotExisting(path, requiredFeatures)
    else:
        return getDataNotExisting(path, requiredFeatures)


if __name__ == '__main__':
    from features.featuresToRequiredDict import featuresToRequiredDict
    path = "..\..\\verySmalldataSet\\"
    f = ['hip.Ax.min', 'hip.Vx.av', 'ankle.simple_sg_ncor.maxDist',
         'ankle.cwt_butter_cor.maxDist', 'head.fout.ief']
#     f = ['ankle.Ax.min', 'ankle.Vx.av','hip.simple_nosmooth.maxDist',
#         'hip.cwt_butter_cor.maxDist', 'head.fout.ief']
    requiredFeatures = featuresToRequiredDict(f)
    print(requiredFeatures)
    data = getData(path, requiredFeatures, False)
    print (data)
