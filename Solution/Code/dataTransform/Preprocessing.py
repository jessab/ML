'''
Created on 2-dec.-2013

@author: Koen
'''

import pylab

import accproc as ac
from dataTransform.accproc import preprocessGCDC
import numpy as np


def moveAv(ar, window, n):
    if n == 1:
        return [np.average(ar[i:i + window]) for i in range(len(ar) - window)]
    else:
        return [np.average(ar[i:i + window]) for i in range(len(ar) - window)
                if np.mod(i, n) == 0]


def moveVar(ar, window):
    return [np.var(ar[i:i + window]) for i in range(len(ar) - window)]


def filterRun3(data, hip):
    vals = data.Atotal.values
    window = 400
    checkInterval = 100
    safetygap = 800
    mvars = moveVar(vals, window)

    # #
#     mvars2 =mvars + [0]*(len(vals)-len(mvars))
#     data['vars'] = mvars2
    # #

    possibilities = []
    curSi = 0
    nbGoodsInARow = 0
    nbBadsInThisSeries = 0
    minGoodsInARow = 4
    maxFracOfBads = 0.05
    minLength = int(3 * safetygap / checkInterval)
    if(hip):
        minvar = 0.05
    else:
        minvar = 0.2

    for i in range(int(len(mvars) / checkInterval)):
        v = np.average(mvars[i * checkInterval:(i + 1) * checkInterval])
        if v > minvar:
            nbGoodsInARow += 1
        else:
            nbBadsInThisSeries += 1
            if (nbGoodsInARow < minGoodsInARow):
                l = i + 1 - curSi
                if ((l > minLength)
                    & ((nbBadsInThisSeries - 1) / l < maxFracOfBads)):
                    possibilities.append((curSi, i))
                nbBadsInThisSeries = 0
                curSi = i + 1
            nbGoodsInARow = 0

    minx, maxx = possibilities[np.argmax(map(lambda (mn, mx):mx - mn,
                                             possibilities))]
    minx = minx * checkInterval + safetygap
    maxx = maxx * checkInterval - safetygap

#     decision = [0]*minx+[1]*(maxx-minx)
#     decision+= [0]*(len(vals)-len(decision))
#     data['decision'] = decision

    return data[minx:maxx]
#     return data


def filterRun(data):
    peaks = ac.detectPeaksGCDC(data, "Atotal", smooth={'type':'hilbert', 'window':64})
    peaks = zip(*peaks)
    xset = peaks[0]
    yset = peaks[1]

    maxy = max(yset)
    miny = 0.3 * maxy
    xset = [xset[i] for i in range(len(xset)) if yset[i] > miny]
    yset = [y for y in yset if y > miny]

#     window_size = 6
    xcandidate = []
    avgDis = (xset[-1] - xset[0]) / (len(xset) - 1)
    for i in range(len(xset) - 1):  # window_size):
#         sampleXset = xset[i:i+window_size]
#         avg = sum(sampleXset)/window_size
#         maxdiff = max([abs(x-avg)
#             for x in sampleXset])/(sampleXset[-1] - sampleXset[0])
        diff = xset[i + 1] - xset[i]
        if (diff / avgDis < 2.50):  # maxdiff < 0.60):
            xcandidate.append(xset[i])
        elif (xcandidate and diff / avgDis > 5.00):  # maxdiff > 0.80):
            break

    maxx = xcandidate[-1]
    minx = xcandidate[0]

    data = data[minx:maxx]
    return data

if __name__ == '__main__':
    subjects = ['Vreni', 'Annick', 'Tina', 'Tinne']
    subjects = ['Ann', 'Emmy', 'Floor']
    subjects = ['Hanne', 'Jolien', 'Laura']
    subjects = ['Mara', 'Nina', 'Sofie', 'Yllia']

    for sub in subjects:
        print(sub)
        for i in range(9):
            nb = int(i + 1)
            print(nb)
            datadir = "..\..\Runs\\" + sub + "\heup\DATA-00" + `nb` + ".csv"
            try:
                data = ac.readGCDCFormat(datadir)
                data = preprocessGCDC(data)
                # data.plot()
                try:
                    data = filterRun3(data, True)
                    data.plot()
                except:
                    print("failed")
            except:
                continue

    pylab.show()
