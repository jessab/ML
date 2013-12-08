'''
Created on 5-dec.-2013

@author: jessa
'''

import pandas as pd
import dataTransform.accproc as ac
import dataTransform.Preprocessing as pp
import features.FeatureExtraction as fa
import sys

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
        data = pp.filterRun3(data);
    except:
        return None
#     data = ac.preprocessGCDC(data)
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

def questionMarkToNaN(val):
    if "?" in val:
        return float('NaN')
    else:
        return float(val.strip())
    
def ynToTF(val):
    if "y" in val:
        return True
    else:
        return False

def loadData(path):
    metadata = loadMetaData(path)
    metadata['Features']= metadata.apply(lambda row : getFeatures(path, row['Name'],row['Nb']),axis=1)
    metadata = metadata[metadata.apply(lambda x: x['Features'] is not None, axis=1)]
    metadata['Sec'] =metadata.apply(lambda x : questionMarkToNaN(x['Sec'] ),axis=1)
    metadata['Trained'] =metadata.apply(lambda x : ynToTF(x['Trained'] ),axis=1)
    metadata['Nb']=metadata['Nb'].astype(int)
    index = pd.MultiIndex.from_arrays([range(len(metadata.index))])
    metadata.index = index
    print(metadata.Features)
    print(metadata)
    metadata.to_csv(path+"data.csv", sep=";")
    return metadata


def main(checkForExistingData=True, path="..\data\Runs\\"):
    path=checkPath(path)
    
    if(checkForExistingData) :
        try :
            data = pd.read_csv(path+"data.csv", sep=";", index_col=0)
            return data
        except:
            return loadData(path)
        
    return loadData(path)
 


if __name__ == '__main__':
    args = sys.argv
    
    hasDataPath = False
    hasCheck = False
    
    nextV=None
    
    for i in range(len(args)):
        val = args[i]
        if val=="datapath":
            nextV = val
        elif val=="checkexisting":
            nextV = val
        elif nextV=="datapath":
            dataPath=val
            hasDataPath=True
        elif nextV=="checkexisting":
            check=val
            hasCheck=True
            
    if hasDataPath & hasCheck:
        main(check,dataPath)
    
    elif hasDataPath:
        main(datapath=dataPath)
    
    elif hasCheck:
        main(checkForExistingData=check)
        
    else: main()
    