'''
Created on 5-dec.-2013

@author: Koen
'''
def getVelocity(data):
    pass
    
    
def get1DVel(time,accSet,peaks):
    velocity = []
    for i, t in enumerate(time[1:]):
        if (t == peaks[0]):
            velocity.append(0)
            peaks.pop(0)
        else:
            velocity.append(velocity[-1] + (t-time(i-1))*(accSet[i] - accSet[i-1])/2)