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
    print("\nSVM: trained-surface\n")
    evalSVM(data, True,True)
    print("\nDT: trained/not trained\n")
    evalDT(data, True,False)
    print("\nDT: surface\n")
    evalDT(data, False,True)
    print("\nDT: trained-surface\n")
    evalDT(data, True,True)
    print("\nKNN: trained/not trained\n")
    evalKNN(data, True,False)
    print("\nKNN: surface\n")
    evalKNN(data, False,True)
    print("\nKNN: trained-surface\n")
    evalKNN(data, True,True)
    print("\nLR: trained/not trained\n")
    evalLR(data, True,False)
    print("\nLR: surface\n")
    evalLR(data, False,True)
    print("\nLR: trained-surface\n")
    evalLR(data, True,True)
    
    pylab.show()

def evalSVM(data, classifyTrained, classifySurface):
    classifier = cl.classifyDataSVM(data, classifyTrained, classifySurface)
    classifier.crossValidation()
    classifier.showProperties()
#     classifier.showSupportVectors()
#     classifier.showSelectedFeatures()
    classifier.plotDecisionSurface()
    
def evalDT(data, classifyTrained, classifySurface):
    classifier = cl.classifyDataDT(data, classifyTrained, classifySurface)
    classifier.crossValidation()
#     classifier.showFeatureImportances()
    classifier.createTreePdf()
    
def evalKNN(data, classifyTrained, classifySurface):
    classifier = cl.classifyDataKNN(data, classifyTrained, classifySurface)
    classifier.crossValidation()
    classifier.showKNeighborsGraph()
    
def evalLR(data, classifyTrained, classifySurface):
    classifier = cl.classifyDataLR(data, classifyTrained, classifySurface)
    classifier.crossValidation()
    
def predict(data, samples, classifier='LogReg', classification='combined'):
    """
    Learns the data-set with the given classifier and gives a prediction for each of the samples.
    """
    if (classification=='trained'):
        classifyTrained = True
        classifySurface = False
    elif (classification=='surface'):
        classifyTrained = False
        classifySurface = True
    else:
        classifyTrained = True
        classifySurface = True
    
    if (classifier=='SVM'):
        clf = cl.classifyDataSVM(data, classifyTrained, classifySurface)
    elif (classifier=='DT'):
        clf = cl.classifyDataDT(data, classifyTrained, classifySurface)
    elif (classifier=='KNN'):
        clf = cl.classifyDataKNN(data, classifyTrained, classifySurface)
    elif (classifier=='LogReg'):
        clf = cl.classifyDataLR(data, classifyTrained, classifySurface)
    
    predictions = [clf.predict(s) for s in samples]
    return predictions

if __name__ == '__main__':
    args = sys.argv
    if len(args)>1:
        main(args[1])
    else :
        main()