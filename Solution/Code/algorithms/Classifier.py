'''
Created on 5-dec.-2013

@author: Koen
'''
from sklearn import svm, cross_validation, tree, datasets
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
from sklearn.externals.six import StringIO  
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import Imputer
import matplotlib.pyplot as plt
from matplotlib import colors
import tools.Tools as tls
import numpy as np

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
    classifier = classifierClass(samples,names,classifications)
    
    
    return classifier

def classifyDataDT(data, classifyTrained, classifySurface):
    return classifyData(data, classifyTrained, classifySurface, DTClassifier)

def classifyDataSVM(data, classifyTrained, classifySurface):
    return classifyData(data, classifyTrained, classifySurface, SVMClassifier)

def classifyDataKNN(data,classifyTrained, classifySurface):
    return classifyData(data, classifyTrained, classifySurface, KNNClassifier)


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
        scores = cross_validation.cross_val_score(self.getClf(), self.getSamples(), self.getClassifications())
        print("Accuracy: \n mean:%f \n std:%f\n" % (scores.mean(), scores.std()))
    
class SVMClassifier(Classifier):
    
    def __init__(self, samples, featureNames, classifications):
        self.clf = svm.SVC()
        Classifier.__init__(self, samples, featureNames, classifications)
        
    def getClf(self):
        return self.clf
    
    def showSupportVectors(self):
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
    
    def showFeatureImportances(self):
        featureArray = self.getClf().feature_importances_
        print("Feature importance:")
        for i,feature in enumerate(featureArray):
            if (feature != 0):
                print(" %s:\t%f" % (self.names[i], feature))
     
    def createTreePdf(self):
        try:
            import pydot
        except:
            return
        dot_data = StringIO()
        tree.export_graphviz(self.getClf(), out_file = dot_data, feature_names=self.names)
        graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
        graph.write_pdf("tree.pdf") 
    
class KNNClassifier(Classifier):
    def __init__(self, samples, featureNames, classifications,k=5):
        self.clf = KNeighborsClassifier(n_neighbors=k, weights='distance')
        Classifier.__init__(self, samples, featureNames, classifications)
        
    def getClf(self):
        return self.clf
    
    def showKNeighborsGraph(self):
        graph = self.getClf().kneighbors_graph(self.samples)
        graph = graph.todense()
        cmap = colors.ListedColormap(['white', 'black'])
        plt.imshow(graph,cmap)
    
if __name__ == '__main__':
    iris = datasets.load_iris()
    clf = SVMClassifier(iris.data, ["sep len", "pet wdt", "sep len", "pet wdt"], iris.target)
    clf.crossValidation()
#     clf.createTreePdf()
#     clf.showFeatureImportances()
#     clf.showKNeighborsGraph()
    
    