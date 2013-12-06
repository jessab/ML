'''
Created on 6-dec.-2013

@author: jessa
'''

from ast import literal_eval

def getDictArray(series): 
    vals = series.values
    return [literal_eval(dic) for dic in vals]