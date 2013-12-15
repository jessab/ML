'''
Created on 6-dec.-2013

@author: Koen
'''
import Classifier as cl
import sys
from sklearn.feature_extraction.dict_vectorizer import DictVectorizer
try:
    import app.featuresMain as fm
except:
    pass
import pylab
import warnings
warnings.filterwarnings("ignore")

plotSurfaces=True
showSVM = True
showDT = True
showKNN = True
showLR = True


def main(data=None, selectFeatures='all'):
    if (data is None):
        data = fm.main()

    if 'RFECV' in selectFeatures:
        showDT = False
        showKNN = False

    if (showSVM):
        print("\nSVM: trained/not trained")
        evalSVM(data, True, False, selectFeatures)
        print("\nSVM: surface")
        evalSVM(data, False, True, selectFeatures)
        print("\nSVM: trained-surface")
        evalSVM(data, True, True, selectFeatures)
        pylab.show()
    if (showDT):
        print("\nDT: trained/not trained")
        evalDT(data, True, False, selectFeatures)
        print("\nDT: surface")
        evalDT(data, False, True, selectFeatures)
        print("\nDT: trained-surface")
        evalDT(data, True, True, selectFeatures)
        pylab.show()
    if (showKNN):
        print("\nKNN: trained/not trained")
        evalKNN(data, True, False, selectFeatures)
        print("\nKNN: surface")
        evalKNN(data, False, True, selectFeatures)
        print("\nKNN: trained-surface")
        evalKNN(data, True, True, selectFeatures)
        pylab.show()
    if (showLR):
        print("\nLR: trained/not trained")
        evalLR(data, True, False, selectFeatures)
        print("\nLR: surface")
        evalLR(data, False, True, selectFeatures)
        print("\nLR: trained-surface")
        evalLR(data, True, True, selectFeatures)
        pylab.show()


def evalSVM(data, classifyTrained, classifySurface, selectFeatures):
    classifier = cl.classifyDataSVM(data, classifyTrained,
                                    classifySurface, selectFeatures)
    classifier.crossValidation()
#     classifier.showProperties()
#     classifier.showSupportVectors()
#     classifier.showSelectedFeatures()
    if (plotSurfaces):
        classifier.plotDecisionSurface()


def evalDT(data, classifyTrained, classifySurface, selectFeatures):
    classifier = cl.classifyDataDT(data, classifyTrained,
                                   classifySurface, selectFeatures)
    classifier.crossValidation()
#     classifier.showFeatureImportances()
    classifier.createTreePdf()
    if (plotSurfaces):
        classifier.plotDecisionSurface()


def evalKNN(data, classifyTrained, classifySurface, selectFeatures):
    classifier = cl.classifyDataKNN(data, classifyTrained,
                                    classifySurface, selectFeatures)
    classifier.crossValidation()
#     classifier.showKNeighborsGraph()
    if (plotSurfaces):
        classifier.plotDecisionSurface()


def evalLR(data, classifyTrained, classifySurface, selectFeatures):
    classifier = cl.classifyDataLR(data, classifyTrained,
                                   classifySurface, selectFeatures)
    classifier.crossValidation()
    if (plotSurfaces):
        classifier.plotDecisionSurface()


def predict(data, samples, classifier='SVM',
            classification='combined', selectFeatures=('CUK', 10)):
    """
    Learns the data-set with the given classifier and
    gives a prediction for each of the samples.
    """
    if (classification == "trained"):
        classifyTrained = True
        classifySurface = False
    elif (classification == "surface"):
        classifyTrained = False
        classifySurface = True
    else:
        classifyTrained = True
        classifySurface = True
    if (classifier == "SVM"):
        clf = cl.classifyDataSVM(data, classifyTrained,
                                 classifySurface, selectFeatures)
    elif (classifier == "DT"):
        clf = cl.classifyDataDT(data, classifyTrained,
                                classifySurface, selectFeatures)
    elif (classifier == "KNN"):
        clf = cl.classifyDataKNN(data, classifyTrained,
                                 classifySurface, selectFeatures)
    elif (classifier == "LogReg"):
        clf = cl.classifyDataLR(data, classifyTrained,
                                classifySurface, selectFeatures)
    else:
        print (str(classifier) + " is not a valid option")
        
    [samples, featureNames] = cl.extractData(samples,False)
    
    indices = [featureNames.index(feature) for feature in clf.getFeatureNames()]
    samples = samples[:,indices]
    
    predictions = [clf.predict(s) for s in samples]
    return predictions


if __name__ == '__main__':
    args = sys.argv
    if len(args)>2:
        main(args[1],args[2])
    elif len(args)>1:
        main(args[1])
    else:
        main()
