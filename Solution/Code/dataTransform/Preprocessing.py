'''
Created on 2-dec.-2013

@author: Koen
'''
import accproc as ac
import pylab
import os
from dataTransform.accproc import preprocessGCDC


def filterRun(data):
    peaks = ac.detectPeaksGCDC(data, "Atotal",smooth={'type':'hilbert','window':64})
    peaks = zip(*peaks)
    xset = peaks[0]
    yset = peaks[1]
        
    maxy = max(yset)
    miny = 0.3*maxy
    xset = [xset[i] for i in range(len(xset)) if yset[i] > miny]
    yset = [y for y in yset if y > miny]
        
#     window_size = 6
    xcandidate = []
    avgDis = (xset[-1]-xset[0])/(len(xset)-1);
    for i in range(len(xset)-1): #window_size):
#         sampleXset = xset[i:i+window_size]
#         avg = sum(sampleXset)/window_size
#         maxdiff = max([abs(x-avg) for x in sampleXset])/(sampleXset[-1] - sampleXset[0])
        diff = xset[i+1]-xset[i];
        if (diff/avgDis < 2.50):#maxdiff < 0.60) : 
            xcandidate.append(xset[i])
        elif (xcandidate and diff/avgDis > 5.00): #maxdiff > 0.80):
            break
        
    maxx = xcandidate[-1]
    minx = xcandidate[0]
        
    data = data[minx:maxx]
    return data

   

   
   
if __name__ == '__main__':
    
    subject = "Vreni"
    plaats = "enkel"
    fdir = getDir(subject, plaats);
    for i in range(len(os.listdir(fdir))):
        datadir = fdir + "DATA-00"+str(i+1) + ".csv"
        data = ac.readGCDCFormat(datadir)
        data = preprocessGCDC(data)
        data.plot()
        try:
            data = filterRun(data);
        except:
            continue
         
        data.plot()
    pylab.show()
 

