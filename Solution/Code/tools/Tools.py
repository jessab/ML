'''
Created on 6-dec.-2013

@author: jessa
'''

from ast import literal_eval

def getDictArray(series): 
    vals = series.values
    return [literal_eval(dic) for dic in vals]

def getFun(data, func, prefix):
    features = data.apply(func, axis=0)
    features.rename(lambda x: prefix+ '.'+ x,inplace=True)
    return features.to_dict()

def getCoVars(data,prefix,includeVar=True):
    cov = data.cov()
    
    res = dict()
    
    cols = cov.columns.values
    rows = cov.index.values
    done = []
    
    for col in cols:
        if not includeVar:
            done+=col
        for row in rows:
            if row not in done :
                if (row>col):
                    name = col+row
                else :
                    name = row+col
                res[prefix+'.'+name+'.covar']=cov[col][row]
        if includeVar:
            done+=col
    
    return res