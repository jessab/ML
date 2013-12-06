'''
Created on 6-dec.-2013

@author: jessa
'''

import featuresMain as fm
import sys

def main(savepath="data\Runs\data.txt",datapath="data\Runs\\"):
    data = fm.main(datapath)
    data.to_pickle(savepath)
    
    

if __name__ == '__main__':
    args = sys.argv
    
    hasDataPath = False
    hasSavePath = False
    
    next=None
    
    for i in range(len(args)):
        val = args[i]
        if val=="datapath":
            next = val
        elif val=="savepath":
            next = val
        elif next=="datapath":
            dataPath=val
            hasDataPath=True
        elif next=="savepath":
            savePath=val
            hasSavePath=True
            
    if hasDataPath & hasSavePath:
        main(savePath,dataPath)
    
    elif hasDataPath:
        main(datapath=dataPath)
    
    elif hasSavePath:
        main(savepath=savePath)
        
    else: main()
    