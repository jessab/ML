'''
Created on 5-dec.-2013

@author: jessa
'''

import pandas as pd
import dataTransform.accproc as ac
import dataTransform.Preprocessing as pp
import features.FeatureExtraction as fa
import sys
from pandas.core.config import is_int

def loadMetaData(path):
    filename = path + "metadata.csv"
    df = pd.io.parsers.read_csv(filename,
                                  names=["Name","Nb","Trained","Surface","Sec"],
                                  skiprows=2,
                                  sep = ";")
    df=df.dropna(thresh = 3)
    
    return df

def getDir(path, subject, plaats, nb):
    return path + subject + "\\" + plaats + "\\" + "DATA-00"+str(int(nb)) + ".csv"

def getData(path,name,nb) :
    plaats = "enkel"
    datadir = getDir(path, name, plaats,nb);
    try:
        data = ac.readGCDCFormat(datadir)
    except:
        return None
    data = ac.preprocessGCDC(data)
    try:
        data = pp.filterRun(data);
        return data
    except:
        return None
    
def getFeatures(path,name,nb) :
    data = getData(path,name,nb)
    if data is None:
        return None
    features = fa.extract(data)
    return features


def checkPath(path):
    #if not ends on \ then add it
    return path

def main(path="data\Runs\\"):
    path=checkPath(path)
    
    metadata = loadMetaData(path)
    metadata['Features']= metadata.apply(lambda row : getFeatures(path, row['Name'],row['Nb']),axis=1)
    metadata = metadata[metadata.apply(lambda x: x['Features'] is not None, axis=1)]
    index = pd.MultiIndex.from_arrays([range(len(metadata.index))])
    metadata.index = index
    print(metadata.Features)
    print(metadata)
    return metadata

if __name__ == '__main__':
    args = sys.argv
    if len(args)>1:
        main(args[1])
    else :
        main()