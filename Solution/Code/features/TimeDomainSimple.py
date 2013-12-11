'''
Created on 5-dec.-2013

@author: jessa
'''

import numpy as np
from tools.Tools import getFun, getCoVars

def posFeatures():
    return {
        'av' : (np.average,True),
        'covar': (getCoVars,False),
        'min': (np.min,True),
        'max': (np.max,True),
        'median': (np.median,True)
    }
    
def posCols():
    return ['Ax','Ay','Az','Atotal']

def checkRequiredFeatures(requiredFeatures):
    generatedFeatures = {'cols':posCols(), 'features':posFeatures().keys()}
    if requiredFeatures is None:
        requiredFeatures = generatedFeatures
    generatedFeatures.update(requiredFeatures)
    generatedFeatures['cols']= [col for col in generatedFeatures['cols'] if col in posCols()]
    generatedFeatures['features']= [f for f in generatedFeatures['features'] if f in posFeatures().keys()]
    
    return generatedFeatures
    
    

def getSimpleTimeDomainFeatures(data, requiredFeatures=None):
    requiredFeatures = checkRequiredFeatures(requiredFeatures)
    data = data[requiredFeatures['cols']]
    
    features = dict()
    for f in requiredFeatures['features']:
        fun,useGetFun = posFeatures()[f]
        if useGetFun:
            ff = getFun(data,fun,f)
        else :
            ff = fun(data,f)
        features.update(ff)
        
    return features

if __name__ == '__main__':
    import dataTransform.accproc as ac
    import dataTransform.Preprocessing as pp
    for i in range(9):
        nb = int(i+1)
        if nb== 4:
            data = ac.readGCDCFormat("..\data\Runs\Tina\enkel\DATA-00" + `nb` + ".csv")
            data = ac.preprocessGCDC(data)
            filtered = pp.filterRun3(data)
            print(getSimpleTimeDomainFeatures(data, {'cols':['Atotal'],'features':['covar','min']}))