'''
Created on 6-dec.-2013

@author: Koen
'''
import Classifier as cl
import sys
import app.featuresMain as fm

def main(path=""):
    if (path):
        data = fm.main(True,path)
    else:
        data = fm.main()
    evalSVM(data, True,False)

def evalSVM(data, classifyTrained, classifySurface):
    classifier = cl.classifyDataSVM(data, classifyTrained, classifySurface);
    classifier.crossValidation()
    classifier.getSupportVectors()
    
def evalDT(data, classifyTrained, classifySurface):
    classifier = cl.classifyDataDT(data, classifyTrained, classifySurface);
    classifier.crossValidation()
    classifier.getFeatureImportances()
    classifier.createTreePdf()
    
if __name__ == '__main__':
    args = sys.argv
    if len(args)>1:
        main(args[1])
    else :
        main()