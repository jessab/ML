'''
Created on 6-dec.-2013

@author: jessa
'''

import app.featuresMain as fm
import sys

def main(savepath="data\Runs\data.csv",datapath="data\Runs\\"):
    data = fm.main(False,datapath)
    data.to_csv("..\data\Runs\data.csv", sep=";")
    # Read with:
    #    data = pd.read_csv(savepath, sep=";", index_col=1)
    

if __name__ == '__main__':
    args = sys.argv
    
    hasDataPath = False
    hasSavePath = False
    
    nextV=None
    
    for i in range(len(args)):
        val = args[i]
        if val=="datapath":
            nextV = val
        elif val=="savepath":
            nextV = val
        elif nextV=="datapath":
            dataPath=val
            hasDataPath=True
        elif nextV=="savepath":
            savePath=val
            hasSavePath=True
            
    if hasDataPath & hasSavePath:
        main(savePath,dataPath)
    
    elif hasDataPath:
        main(datapath=dataPath)
    
    elif hasSavePath:
        main(savepath=savePath)
        
    else: main()
    