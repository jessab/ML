'''
Created on 5-dec.-2013

@author: jessa
'''

from ast import literal_eval
import sys

from DataLoader import getData
from features.featuresToRequiredDict import featuresToRequiredDict


def checkPath(path):
    if path[-1] != "\\":
        path += "\\"
    return path


def main(useExisting=True, path="..\..\Runs\\", features=None):
    path = checkPath(path)

    if features is not None:
        features = literal_eval(features)
        if type(features) == list:
            features = featuresToRequiredDict(features)

    data = getData(path, features, useExisting)
    print(data.Features)
    print(data)
    return data


if __name__ == '__main__':
    args = sys.argv

    features = None
    dataPath = "..\..\Runs\\"
    useExisting = True

    nextV = None

    for i in range(len(args)):
        val = args[i]
        if val == "datapath":
            nextV = val
        elif val == "useExisting":
            nextV = val
        elif val == "features":
            nextV = val

        elif nextV == "datapath":
            dataPath = val
        elif nextV == "useExisting":
            useExisting = val
        elif nextV == "features":
            features = val

    main(useExisting, dataPath, features)
