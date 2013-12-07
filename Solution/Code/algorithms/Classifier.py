'''
Created on 5-dec.-2013

@author: Koen
'''
from sklearn import svm, cross_validation, tree, datasets
from sklearn.externals.six import StringIO  
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import Imputer
import tools.Tools as tls
import numpy as np
import pydot

def surfaces():
    return ["Asphalt","Track", "Woodchip"]
    
def classifyData(data, classifyTrained, classifySurface, classifierClass):
    features = tls.getDictArray(data.Features)
    vec = DictVectorizer()
    samples = vec.fit_transform(features)
    imp = Imputer(missing_values='NaN', strategy='mean')
    imp.fit(samples)
    samples = imp.transform(samples)
    
    names = vec.get_feature_names()
    
    if (classifyTrained):
        classifications = data.Trained
    elif (classifySurface):
        classifications = data.Surface
        classifications = [surfaces().index(x.strip()) for x in classifications]
        classifications = np.asarray(classifications)
    else:
        raise NotImplementedError("Combined classification has not yet been implemented")
    print(classifications)
    classifier = classifierClass(samples,names,classifications)
    
    
    return classifier

def classifyDataDT(data, classifyTrained, classifySurface):
    return classifyData(data, classifyTrained, classifySurface, DTClassifier)

def classifyDataSVM(data, classifyTrained, classifySurface):
    return classifyData(data, classifyTrained, classifySurface, SVMClassifier)
    
class Classifier(object):
    '''
    classdocs
    '''
    def __init__(self,samples,featureNames,classifications):
        self.samples = samples
        self.names = featureNames
        self.classifications = classifications
        
        self.fit()
   
    def getClf(self):
        raise NotImplementedError("Subclass must implement abstract method")
   
    def getSamples(self):
        return self.samples
   
    def getClassifications(self):
        return self.classifications
   
    def fit(self):
        self.getClf().fit(self.getSamples(),self.getClassifications())
        
    def predict(self,sample):
        return self.getClf().predict(sample)
    
    def score(self,samples,classifications):
        return self.getClf().score(samples, classifications)
        
    def crossValidation(self):
        scores = cross_validation.cross_val_score(self.getClf(), self.getSamples(), self.getClassifications(),cv=10)
        print("Accuracy: \n mean:%f \n std:%f\n" % (scores.mean(), scores.std()))
    
class SVMClassifier(Classifier):
    
    def __init__(self, samples, featureNames, classifications):
        self.clf = svm.SVC()
        Classifier.__init__(self, samples, featureNames, classifications)
        
    def getClf(self):
        return self.clf
    
    def getSupportVectors(self):
        svArray = self.getClf().n_support_
        print("Support vectors:")
        for i,svector in enumerate(svArray):
            print(" %i:\t%s" % (i, str(svector)))
    
class DTClassifier(Classifier):
    
    def __init__(self, samples, featureNames, classifications):
        self.clf = tree.DecisionTreeClassifier()
        samples = samples.toarray()
        Classifier.__init__(self, samples, featureNames, classifications)
        
    def getClf(self):
        return self.clf
    
    def getFeatureImportances(self):
        featureArray = self.getClf().feature_importances_
        print("Feature importance:")
        for i,feature in enumerate(featureArray):
            if (feature != 0):
                print(" %s:\t%f" % (self.names[i], feature))
     
    def createTreePdf(self):
        dot_data = StringIO()
        tree.export_graphviz(self.getClf(), out_file = dot_data, feature_names=self.names)
        graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
        graph.write_pdf("tree.pdf") 
    
    
if __name__ == '__main__':
    iris = datasets.load_iris()
    print(iris.target)
    dtclf = SVMClassifier(iris.data, ["sep len", "pet wdt", "sep len", "pet wdt"], iris.target)
    dtclf.crossValidation()
#     dtclf.createTreePdf()
    dtclf.getFeatureImportances()
    
    