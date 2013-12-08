'''
Created on 2-dec.-2013

@author: Koen
'''
import accproc as ac
import pylab
import os
from dataTransform.accproc import preprocessGCDC
import numpy as np

def moveAv(ar, window,n):
    if n==1 :
        return [np.average(ar[i:i+window]) for i in range(len(ar)-window)]
    else :
        return [np.average(ar[i:i+window]) for i in range(len(ar)-window) if np.mod(i,n)==0]
          
def moveVar(ar,window):
    return [np.var(ar[i:i+window]) for i in range(len(ar)-window)]

def filterRun2(data):
    vals = data.Atotal.values
    length = len(vals)
    window = 400
    checkInterval = 100
    safetygap = 800
    averages = moveAv(vals,window,1)
    averages = moveAv(averages,window,checkInterval)
    
    maxav = max(averages)
    limit = maxav/2
    possibilities = []
    curSi=0
    nbGoodsInARow = 0
    nbBadsInThisSeries = 0
    minGoodsInARow = 4
    maxFracOfBads = 0.05
    minLength = int(3*safetygap/checkInterval)
     
    for i in range(len(averages)) :
        if averages[i]>limit :
            nbGoodsInARow+=1
        else :
            nbBadsInThisSeries+=1
            if nbGoodsInARow<minGoodsInARow:
                l = i+1-curSi
                if (l>minLength) & (nbBadsInThisSeries/l<maxFracOfBads) :
                    possibilities.append((curSi,i))
                nbBadsInThisSeries=0
                curSi=i+1
            nbGoodsInARow=0
             
    minx,maxx = possibilities[np.argmax(map(lambda (mn,mx):mx-mn,possibilities))]
    minx = minx*checkInterval
    maxx = maxx*checkInterval
#             
#     if len(possibilities)>0 :
#         minx,maxx = possibilities[np.argmax(map(lambda (mn,mx):mx-mn,possibilities))]
#         averages = [0]*(minx-1+safetygap)+[1]*((maxx-minx+window-2*safetygap)
#         
#     else :
#         averages = []
    
#     averages+= [0]*(length-len(averages))
            
        
    
   # Set all averages that are smaller than the max to zero
   # Extract the possibilities as the oppeenvolgende ones
   # Choose best possibilitie(longest)
   # Remove begin and end (2s)
    
#     data['smooth']=averages
    return data[minx+safetygap:maxx-safetygap]
#     return data


def filterRun3(data):
    vals = data.Atotal.values
    length = len(vals)
    window = 400
    checkInterval = 100
    safetygap = 800
    vars = moveVar(vals,window)
    #vars = moveAv(vars,checkInterval,checkInterval)
     
    possibilities = []
    curSi=0
    nbGoodsInARow = 0
    nbBadsInThisSeries = 0
    minGoodsInARow = 4
    maxFracOfBads = 0.05
    minLength = int(3*safetygap/checkInterval)
      
    for i in range(int(len(vars)/checkInterval)) :
        v = np.average(vars[i*checkInterval:(i+1)*checkInterval])
        if v>0.2 :
            nbGoodsInARow+=1
        else :
            nbBadsInThisSeries+=1
            if (nbGoodsInARow<minGoodsInARow):
                l = i+1-curSi
                if (l>minLength) & ((nbBadsInThisSeries-1)/l<maxFracOfBads) :
                    possibilities.append((curSi,i))
                nbBadsInThisSeries=0
                curSi=i+1
            nbGoodsInARow=0
             
#     if len(possibilities)==0:
#         vars = []
#      
#     else :
#         minx,maxx = possibilities[np.argmax(map(lambda (mn,mx):mx-mn,possibilities))]
#         minx = minx*checkInterval
#         maxx = maxx*checkInterval
#         vars = [0]*(minx-1+safetygap)+[5]*(maxx-minx-2*safetygap)
#                                                
#     vars+= [0]*(length-len(vars))
#     data['vars']=vars
#     return data
    minx,maxx = possibilities[np.argmax(map(lambda (mn,mx):mx-mn,possibilities))]
    minx = minx*checkInterval+safetygap
    maxx = maxx*checkInterval-safetygap
    
    return data[minx:maxx]

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
    
#     subjects = ["Ann","Annick","Emmy"]
#     subjects = ["Example","Floor","Hanne"]
#     subjects = ["Jolien","Laura","Mara"]
    subjects = ["Nina","Sofie","Tina","Vreni"]
#     subjects = ["Tinne","Vreni","Yllia"]
#     subjects = ["Tina"]
    plaats = "enkel"
    j=0
    
    for subject in subjects : 
        fdir = "..\data\Runs\\"+ subject + "\enkel\\"
        for i in range(len(os.listdir(fdir))):
            j+=1
            datadir = fdir + "DATA-00"+str(i+1) + ".csv"
            data = ac.readGCDCFormat(datadir)
            data = preprocessGCDC(data)
            #data.plot()
            try:
                data = filterRun3(data);
                data.plot()
            except:
                print(`j`+" "+subject + `i`)
                data.plot()
                continue
         
    pylab.show()
 

