'''
Created on 6-dec.-2013

@author: Koen
'''
import Classifier as cl
import sys
try:
    import app.featuresMain as fm
except:
    pass
import pylab
import warnings
warnings.filterwarnings("ignore")

selectFeatures=True
plotSurfaces=False
showSVM = False
showDT = True
showKNN = True
showLR = False

def main(path=""):
    if (path):
        data = fm.main(True,path)
    else:
        data = fm.main()
    if (showSVM):
        print("\nSVM: trained/not trained")
        evalSVM(data, True,False)
        print("\nSVM: surface")
        evalSVM(data, False,True)
        print("\nSVM: trained-surface")
        evalSVM(data, True,True)
        pylab.show()
    if (showDT):
        print("\nDT: trained/not trained")
        evalDT(data, True,False)
        print("\nDT: surface\n")
        evalDT(data, False,True)
        print("\nDT: trained-surface")
        evalDT(data, True,True)
        pylab.show()
    if (showKNN):
        print("\nKNN: trained/not trained")
        evalKNN(data, True,False)
        print("\nKNN: surface\n")
        evalKNN(data, False,True)
        print("\nKNN: trained-surface")
        evalKNN(data, True,True)
        pylab.show()
    if (showLR):
        print("\nLR: trained/not trained")
        evalLR(data, True,False)
        print("\nLR: surface\n")
        evalLR(data, False,True)
        print("\nLR: trained-surface")
        evalLR(data, True,True)
        pylab.show()

def evalSVM(data, classifyTrained, classifySurface):
    classifier = cl.classifyDataSVM(data, classifyTrained, classifySurface,selectFeatures)
    classifier.crossValidation()
#     classifier.showProperties()
#     classifier.showSupportVectors()
#     classifier.showSelectedFeatures()
    if (plotSurfaces):
        classifier.plotDecisionSurface()
    
def evalDT(data, classifyTrained, classifySurface):
    classifier = cl.classifyDataDT(data, classifyTrained, classifySurface,selectFeatures)
    classifier.crossValidation()
#     classifier.showFeatureImportances()
    classifier.createTreePdf()
    if (plotSurfaces):
        classifier.plotDecisionSurface()    

def evalKNN(data, classifyTrained, classifySurface):
    classifier = cl.classifyDataKNN(data, classifyTrained, classifySurface,selectFeatures)
    classifier.crossValidation()
#     classifier.showKNeighborsGraph()
    if (plotSurfaces):
        classifier.plotDecisionSurface()
    
def evalLR(data, classifyTrained, classifySurface):
    classifier = cl.classifyDataLR(data, classifyTrained, classifySurface,selectFeatures)
    classifier.crossValidation()
    if (plotSurfaces):
        classifier.plotDecisionSurface()
    
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
