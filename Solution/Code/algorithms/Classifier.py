'''
Created on 5-dec.-2013

@author: Koen
'''
from sklearn import svm, cross_validation, tree, datasets
from sklearn.externals.six import StringIO  
from sklearn.feature_extraction import DictVectorizer
import pydot 
    
class Classifier(object):
    '''
    classdocs
    '''
    def __init__(self,samples,classifications):
#         vec = DictVectorizer()
#         self.samples = vec.fit_transform(samples)
#         self.names = vec.get_feature_names()
        self.samples = samples
        self.names = ["sepal length","sepal width","petal length","petal width"]
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
        scores = cross_validation.cross_val_score(self.getClf(), self.getSamples(), self.getClassifications(),cv=30)
        print("Accuracy: \n mean:%f \n std:%f\n" % (scores.mean(), scores.std()))
        
    def getFeatureImportances(self):
        featureArray = self.getClf().feature_importances_
        print("Feature importance:")
        for i,feature in enumerate(featureArray):
            print(" %s:\t%f" % (self.names[i], feature))
    
class SVMClassifier(Classifier):
    
    def __init__(self, samples, classifications):
        self.clf = svm.SVC()
        Classifier.__init__(self, samples, classifications)
        
    def getClf(self):
        return self.clf
    
class DTClassifier(Classifier):
    
    def __init__(self, samples, classifications):
        self.clf = tree.DecisionTreeClassifier()
        Classifier.__init__(self, samples, classifications)
        
    def getClf(self):
        return self.clf
     
    def createTreePdf(self):
        dot_data = StringIO()
        tree.export_graphviz(self.getClf(), out_file = dot_data)
        graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
        graph.write_pdf("tree.pdf") 
    
    
if __name__ == '__main__':
    iris = datasets.load_iris()
    dtclf = DTClassifier(iris.data,iris.target)
    dtclf.crossValidation()
    dtclf.createTreePdf()
    dtclf.getFeatureImportances()
    
    