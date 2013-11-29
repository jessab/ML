'''
Created on 29-nov.-2013

@author: Koen
'''
from algorithms.Classification import Classification

class Knearest(object):
    def __init__(self, listOfSamples, k):
        self.listOfSamples = listOfSamples
        self.k=k
        
    def classify(self, sample):
        listOfDistances = []
        for otherSample in self.listOfSamples:
            d = sample.distance(otherSample)
            listOfDistances.append((d,otherSample))
        listOfNeighbours = []
        for _ in range(self.k):
            (m,s) = min(listOfDistances)
            listOfNeighbours.append(s)
            listOfDistances.remove((m,s))
        return self.CombineClassification(listOfNeighbours)
        
    def CombineClassification(self, listOfNeighbours):
        trained = 0
        woodchip = 0
        asfalt = 0
        track = 0
        for sample in listOfNeighbours :
            if(sample.isTrained()):
                trained += 1
            else:
                trained -= 1
            if (sample.getTerrain()=="woodchip"):
                woodchip +=1
            elif (sample.getTerrain()=="asfalt"):
                asfalt+=1
            elif (sample.getTerrain()=="track"):
                track+=1
        if (trained >= 0):
            tr = True
        else:
            tr = False
        m = max(woodchip,asfalt,track)
        if (m == woodchip):
            return Classification(tr,"woodchip")
        elif (m == asfalt):
            return Classification(tr,"asfalt")
        else:
            return Classification(tr,"track")
            
            