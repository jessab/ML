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
    except:
        return None
    data = ac.preprocessGCDC(data)
    return data
    
def getFeatures(path,name,nb) :
    data = getData(path,name,nb)
    if data is None:
        return None
    features = fa.extract(data)
    return features


def checkPath(path):
    if path[-1]!="\\" :
        path+="\\"
    return path

def loadData(path):
    metadata = loadMetaData(path)
    metadata['Features']= metadata.apply(lambda row : getFeatures(path, row['Name'],row['Nb']),axis=1)
    metadata = metadata[metadata.apply(lambda x: x['Features'] is not None, axis=1)]
    index = pd.MultiIndex.from_arrays([range(len(metadata.index))])
    metadata.index = index
    print(metadata.Features)
    print(metadata)
    return metadata


def main(checkForExistingData=True, path="..\data\Runs\\"):
    path=checkPath(path)
    
    if(checkForExistingData) :
        try :
            data = pd.read_csv(path+"data.csv", sep=";", index_col=1)
            return data
        except:
            return loadData(path)
        
    return loadData(path)
 


if __name__ == '__main__':
    args = sys.argv
    
    hasDataPath = False
    hasCheck = False
    
    next=None
    
    for i in range(len(args)):
        val = args[i]
        if val=="datapath":
            next = val
        elif val=="checkexisting":
            next = val
        elif next=="datapath":
            dataPath=val
            hasDataPath=True
        elif next=="checkexisting":
            check=val
            hasCheck=True
            
    if hasDataPath & hasCheck:
        main(check,dataPath)
    
    elif hasDataPath:
        main(datapath=dataPath)
    
    elif hasCheck:
        main(checkForExistingData=check)
        
    else: main()
    