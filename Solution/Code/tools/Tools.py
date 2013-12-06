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