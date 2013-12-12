'''
Created on 5-dec.-2013

@author: Koen
'''
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)

from sklearn import svm, cross_validation, tree, datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals.six import StringIO  
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, RFECV
from sklearn import preprocessing as pp
import pylab as pl
from matplotlib import colors
import tools.Tools as tls
import numpy as np

def surfaces():
    return ["Asphalt","Track", "Woodchip"]

def trainedClasses():
    return ["Not Trained", "Trained"]

def extractData(data):
    features = tls.getDictArray(data.Features)
    vec = DictVectorizer()
    samples = vec.fit_transform(features)
    imp = pp.Imputer(missing_values='NaN', strategy='mean')
    imp.fit(samples)
    samples = imp.transform(samples)
    samples = pp.scale(samples, with_mean=False)
    featureNames = vec.get_feature_names()
    return [samples,featureNames]

def selectKBestFeatures(samples,classifications,featureNames,nbFeatures=10):
    fs = SelectKBest(k=nbFeatures)
    samples = fs.fit_transform(samples, classifications)
    sup = fs.get_support()
    
    featureNames = [featureNames[i] for (i,s) in enumerate(sup) if s]
    return [samples,featureNames]

def selectBestFeaturesRFECV(samples,classifications,featureNames,classifierClass):
    fs = RFECV(classifierClass.getEstimator())
    samples = fs.fit_transform(samples, classifications)
    sup = fs.get_support()
    
    featureNames = [featureNames[i] for (i,s) in enumerate(sup) if s]
    return [samples,featureNames]

def selectFeatures(samples,classifications,featureNames,classifierClass,nbFeatures=10):
#     [samples,featureNames] = selectBestFeaturesRFECV(samples, classifications, featureNames, classifierClass)
    [samples,featureNames] = selectKBestFeatures(samples, classifications, featureNames, nbFeatures)
    return [samples,featureNames]
    
def selectClassifications(data,classifyTrained,classifySurface):
    if (classifyTrained and classifySurface):
        t = data.Trained
        s = data.Surface
        classifications = [(3*t[i] + surfaces().index(s[i].strip())) for (i,_) in enumerate(t)]
        classifications = np.asarray(classifications)
        classNames = [t + " - "+ s for t in trainedClasses() for s in surfaces()]
    elif (classifyTrained):
        classifications = data.Trained
        classNames = trainedClasses()
    elif (classifySurface):
        classifications = data.Surface
        classifications = [surfaces().index(x.strip()) for x in classifications]
        classifications = np.asarray(classifications)
        classNames = surfaces()
    return [classifications,classNames]
    
def classifyData(data, classifyTrained, classifySurface, classifierClass, featuresSelect):
    [samples,featureNames] = extractData(data)
    [classifications, classNames] = selectClassifications(data, classifyTrained, classifySurface)
    
    if (featuresSelect):
        [samples,featureNames] = selectFeatures(samples, classifications, featureNames,classifierClass)
    classifier = classifierClass(samples,featureNames,classifications,classNames)
    
    return classifier

def classifyDataDT(data, classifyTrained, classifySurface):
    return classifyData(data, classifyTrained, classifySurface, DTClassifier,True)

def classifyDataSVM(data, classifyTrained, classifySurface):
    return classifyData(data, classifyTrained, classifySurface, SVMClassifier,False)

def classifyDataKNN(data,classifyTrained, classifySurface):
    return classifyData(data, classifyTrained, classifySurface, KNNClassifier,False)

def classifyDataLR(data,classifyTrained, classifySurface):
    return classifyData(data, classifyTrained, classifySurface, LRClassifier,False)

class Classifier(object):
    '''
    classdocs
    '''
    def __init__(self,samples,featureNames,classifications, classificationNames):
        self.samples = samples
        self.featureNames = featureNames
        self.classifications = classifications
        self.classNames = classificationNames
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
        p = self.getClf().predict(sample)
        return self.classNames[p]
    
    def score(self,samples,classifications):
        return self.getClf().score(samples, classifications)
        
    def crossValidation(self):
        scores = cross_validation.cross_val_score(self.getClf(), self.getSamples(), self.getClassifications())
        print("Accuracy: \n mean:%f \n std:%f\n" % (scores.mean(), scores.std()))
        
    def showSelectedFeatures(self):
        print("Selected features:")
        for fn in self.featureNames:
            print(fn)
            
    def showProperties(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    @staticmethod     
    def getEstimator():
        raise NotImplementedError("Subclass must implement abstract method")
    
    def plotDecisionSurface(self):
        classifierClass = self.__class__
        [samples,featureNames] = selectFeatures(self.samples, self.classifications, self.featureNames,classifierClass,2)
        clf = classifierClass(samples,featureNames,self.classifications,self.classNames)
        
        X = samples
        if (type(X) == np.ndarray):
            X = np.matrix(self.samples)
        Y = self.classifications
        h=0.01
        
        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))
        
        Z = clf.getClf().predict(np.c_[xx.ravel(), yy.ravel()])
        
        Z = Z.reshape(xx.shape)
        
        ttl = self.classifierName() + "  " +self.featureNames[0] + " - " + self.featureNames[1]
        
        colors = pl.cm.Paired
        
        fig = pl.figure()
        ax = fig.add_subplot(111, title=ttl)
        ax.contourf(xx, yy, Z, cmap=colors)
        pl.axis('off')
        
        xas = np.asarray(X[:, 0])
        xas = [xas[()][i,0] for i in range(xas[()].shape[0])]
        yas = np.asarray(X[:, 1])
        yas = [yas[()][i,0] for i in range(yas[()].shape[0])]
        ax.scatter(xas, yas, c=Y, cmap=colors)
        
        self.fit()
        
    def classifierName(self):
        return "undefined"
        
    
class SVMClassifier(Classifier):
    
    def __init__(self, samples, featureNames, classifications, classificationNames):
        self.clf = svm.SVC(kernel='linear',C=0.8)
        Classifier.__init__(self, samples, featureNames, classifications, classificationNames)
        
    def getClf(self):
        return self.clf
    
    def showProperties(self):
        self.showSupportVectors()
    
    def showSupportVectors(self):
#         svArray = self.getClf().n_support_
#         print("Support vectors:")
#         for i,svector in enumerate(svArray):
#             print(" %i:\t%s" % (i, str(svector)))
        import heapq
        import operator
        svArray = self.getClf().coef_
        svArray = svArray.toarray()
        for i,fa in enumerate(svArray):
            if (i < len(self.classNames)):
                print(self.classNames[i] + ":")
                bestFeatures = heapq.nlargest(5, enumerate(fa), operator.itemgetter(1))
                bestFeatures = [self.featureNames[x] for x in zip(*bestFeatures)[0]]
                for f in bestFeatures:
                    print("  " +f)
            
    @staticmethod     
    def getEstimator():
        return svm.SVR(kernel='linear')
    
    def classifierName(self):
        return "SVM"
    
class DTClassifier(Classifier):
    
    def __init__(self, samples, featureNames, classifications, classificationNames):
        self.clf = tree.DecisionTreeClassifier(min_samples_split=4, max_depth=4)
        samples = samples.toarray()
        Classifier.__init__(self, samples, featureNames, classifications, classificationNames)
        
    def getClf(self):
        return self.clf
    
    def showFeatureImportances(self):
        featureArray = self.getClf().feature_importances_
        print("Feature importance:")
        for i,feature in enumerate(featureArray):
            if (feature != 0):
                print(" %s:\t%f" % (self.featureNames[i], feature))
     
    def createTreePdf(self):
        try:
            import pydot
        except:
            return
        dot_data = StringIO()
        tree.export_graphviz(self.getClf(), out_file = dot_data, feature_names=self.featureNames)
        graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
        graph.write_pdf("tree.pdf") 
        
    @staticmethod     
    def getEstimator():
        return tree.DecisionTreeRegressor()
    
    def classifierName(self):
        return "DT"
    
class KNNClassifier(Classifier):
    def __init__(self, samples, featureNames, classifications, classificationNames, k=5):
        self.clf = KNeighborsClassifier(n_neighbors=k, weights='distance')
        Classifier.__init__(self, samples, featureNames, classifications, classificationNames)
        
    def getClf(self):
        return self.clf
    
    def showKNeighborsGraph(self):
        graph = self.getClf().kneighbors_graph(self.samples)
        graph = graph.todense()
        cmap = colors.ListedColormap(['white', 'black'])
        fig = pl.figure()
        ax = fig.add_subplot(111, title="KNN: nearest neighbours graph")
        ax.imshow(graph,cmap)
        
    def classifierName(self):
        return "KNN"
        
class LRClassifier(Classifier):
    def __init__(self, samples, featureNames, classifications, classificationNames):
        self.clf = LogisticRegression()
        Classifier.__init__(self, samples, featureNames, classifications, classificationNames)
        
    def getClf(self):
        return self.clf
    
    def classifierName(self):
        return "LogReg"
    
if __name__ == '__main__':
    iris = datasets.load_iris()
    clf = DTClassifier(iris.data, ["sep len", "pet wdt", "sep len", "pet wdt"], iris.target,["red","blue","green"])
    clf.crossValidation()
#     clf.plotDecisionSurface()
#     clf.createTreePdf()
#     clf.showFeatureImportances()
#     clf.showKNeighborsGraph()
    
    