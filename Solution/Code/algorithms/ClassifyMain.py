'''
Created on 6-dec.-2013

@author: Koen
'''
import Classifier as cl
import sys
import app.featuresMain as fm
import pylab

def main(path=""):
    if (path):
        data = fm.main(True,path)
    else:
        data = fm.main()
    print("\nSVM: trained/not trained\n")
    evalSVM(data, True,False)
    print("\nSVM: surface\n")
    evalSVM(data, False,True)
    print("\nDT: trained/not trained\n")
    evalDT(data, True,False)
    print("\nDT: surface\n")
    evalDT(data, False,True)
    print("\nKNN: trained/not trained\n")
    evalKNN(data, True,False)
    print("\nKNN: surface\n")
    evalKNN(data, False,True)
    pylab.show()

def evalSVM(data, classifyTrained, classifySurface):
    classifier = cl.classifyDataSVM(data, classifyTrained, classifySurface)
    classifier.crossValidation()
    classifier.showSupportVectors()
    
def evalDT(data, classifyTrained, classifySurface):
    classifier = cl.classifyDataDT(data, classifyTrained, classifySurface)
    classifier.crossValidation()
    classifier.showFeatureImportances()
    classifier.createTreePdf()
    
def evalKNN(data, classifyTrained, classifySurface):
    classifier = cl.classifyDataKNN(data, classifyTrained, classifySurface)
    classifier.crossValidation()
    classifier.showKNeighborsGraph()
    
if __name__ == '__main__':
    args = sys.argv
    if len(args)>1:
        main(args[1])
    else :
        main()