'''
Created on 5-dec.-2013

@author: Koen
'''
import warnings
from sklearn.linear_model.logistic import LogisticRegression

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)

from sklearn import svm, cross_validation, tree, datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals.six import StringIO
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_selection import SelectKBest, RFECV, f_classif
from sklearn import preprocessing as pp
import pylab as pl
from matplotlib import colors
from scipy import sparse as sprs
import tools.Tools as tls
import numpy as np
from scipy.sparse import csr_matrix


def surfaces():
    return ["Asphalt","Track", "Woodchip"]

def trainedClasses():
    return ["Untrained", "Trained"]

def shouldReplace(a):
    try:
        return np.isnan(a)
    except:
        return False

def extractData(features, examples=None, scaler=None, featureOrder=None, scaling=False):
    vec = DictVectorizer()
    samples = vec.fit_transform(features)
    featureNames = vec.get_feature_names()
    
    if (featureOrder != None):
        indices = [featureNames.index(feature) for feature in featureOrder]
        samples = samples[:, indices]
    imp = pp.Imputer(missing_values='NaN', strategy='mean')
    if (examples == None):
        imp.fit(samples)
    else :
        imp.fit(examples)
    impSamples = imp.transform(samples)
    if (impSamples.shape == samples.shape):
        samples = impSamples
    else:
        print("too few samples to replace missing values, using 0's")
        samples[shouldReplace(samples)]=0
    
#     if (scaler == None):
#         scaler = pp.StandardScaler(with_mean=False)
#         scaler.fit(samples)
#     samples = scaler.transform(samples)
    if (scaling):
        samples = pp.scale(samples,with_mean=False)
    if (sprs.isspmatrix(samples)):
        samples = samples.todense()
    
    return [samples, featureNames,imp,scaler]

def selectKBestFeatures(samples, classifications, featureNames, nbFeatures=10):
    fs = SelectKBest(f_classif, k=nbFeatures)
    samples = fs.fit_transform(samples, classifications)
    sup = fs.get_support()

    featureNames = [featureNames[i] for (i, s) in enumerate(sup) if s]
    scores = fs.scores_
    scores = [s for (i, s) in enumerate(scores) if sup[i]]
    return [samples, featureNames, scores]

def selectBestFeaturesRFECV(samples, classifications,
                            featureNames, classifierClass):
    fs = RFECV(classifierClass.getEstimator())
    if (not sprs.issparse(samples)):
        samples = sprs.csr_matrix(samples)
    samples = fs.fit_transform(samples.toarray(), classifications)
    sup = fs.get_support()
    
    featureNames = [featureNames[i] for (i,s) in enumerate(sup) if s]
    return [samples,featureNames]

def selectKBestUncorrelatedFeatures(samples, classifications,
                                    featureNames, nbFeatures=10):
    k10 = 10 * nbFeatures
    [samples, featureNames, scores] = selectKBestFeatures(samples,
                                    classifications, featureNames, k10)

    if len(featureNames) < k10:
        k10 = len(featureNames)

    isSparse = (type(samples) == csr_matrix)

    if isSparse:
        samples = samples.todense()

    corr = np.corrcoef(samples, rowvar=False)
    sel = []
    for _ in range(nbFeatures):
        if len([s for s in scores if s > 0]) == 0:
            break
        s = np.argmax(scores)
        sel.append(s)
        scores = map(lambda i: scores[i] * (corr[s, i] < 0.2), range(k10))

    samples = np.transpose(samples)
    samples = np.transpose([np.array(samples[j, :]).reshape(-1) for j in sel])
    if isSparse:
        samples = csr_matrix(samples)

    featureNames = [featureNames[i] for i in sel]

    return [samples, featureNames]

def selectFeatures(samples, classifications, featureNames, classifierClass, selectionMethod, silent=False):
    if 'RFECV' in selectionMethod:
        try:
            [samples,featureNames] = selectBestFeaturesRFECV(samples, classifications, featureNames, classifierClass)
            if (not silent):
                print ("Using RFECV feature selection")
        except:
            [samples,featureNames] = selectKBestUncorrelatedFeatures(samples, classifications, featureNames)
            if (not silent):
                print ("Using KBest feature selection with correlation filter")
    else:
        sel, nbFeatures = selectionMethod
        if 'KUC' in sel:
            [samples,featureNames] = selectKBestUncorrelatedFeatures(samples, classifications, featureNames, nbFeatures)
            if (not silent):
                print ("Using KBest feature selection with correlation filter")
        else:
            [samples,featureNames,_] = selectKBestFeatures(samples, classifications, featureNames, nbFeatures)
            if (not silent):
                print ("Using KBest feature selection")
    
    if (not silent):
        print(str(len(featureNames)) + " features selected:")
        if (len(featureNames) > 10):
            [_,fnamelist,_] = selectKBestFeatures(samples, classifications, featureNames, 10)
            for fn in fnamelist:
                print("  " + fn)
            print("  ...")
        else:
            for fn in featureNames:
                print("  " + fn)
    
    return [samples,featureNames] 
    
def selectClassifications(data,classifyTrained,classifySurface):
    if (classifyTrained and classifySurface):
        t = data.Trained
        s = data.Surface
        classifications = [(3 * t[i] + surfaces().index(s[i].strip()))
                           for (i, _) in enumerate(t)]
        classifications = np.asarray(classifications)
        classNames = [t + "&" + s for t in trainedClasses()
                      for s in surfaces()]
    elif (classifyTrained):
        classifications = data.Trained
        classNames = trainedClasses()
    elif (classifySurface):
        classifications = data.Surface
        classifications = [surfaces().index(x.strip())
                           for x in classifications]
        classifications = np.asarray(classifications)
        classNames = surfaces()
    return [classifications, classNames]


def classifyData(data, classifyTrained, classifySurface,
            classifierClass, featuresSelect,scaling=False):
    features = tls.getDictArray(data.Features)
    [samples, featureNames,imputer,scaler] = extractData(features,scaling=scaling)
    [classifications, classNames] = selectClassifications(data,
                                    classifyTrained, classifySurface)

    if (not 'all' in featuresSelect):
        [samples, featureNames] = selectFeatures(samples,
                    classifications, featureNames,
                    classifierClass, featuresSelect)
    else:
        print('Using all features')
    classifier = classifierClass(samples, featureNames,
                                 classifications, classNames)
    classifier.setTransformOperators(imputer,scaler)

    return classifier


def classifyDataDT(data, classifyTrained,
                classifySurface, selectFeatures=('KUC', 10),scaling=True):
    if 'RFECV' in selectFeatures:
        print('RFECV cannot be used in combination with DT')
        raise SystemExit(0)
    return classifyData(data, classifyTrained,
                classifySurface, DTClassifier, selectFeatures,scaling)


def classifyDataSVM(data, classifyTrained,
                classifySurface, selectFeatures=('KUC', 10),scaling=True):
    return classifyData(data, classifyTrained, classifySurface,
                        SVMClassifier, selectFeatures,scaling)


def classifyDataKNN(data, classifyTrained,
                classifySurface, selectFeatures=('KUC', 10),scaling=True):
    if 'RFECV' in selectFeatures:
        print('RFECV cannot be used in combination with KNN')
        raise Exception
    return classifyData(data, classifyTrained, classifySurface,
                        KNNClassifier, selectFeatures,scaling)


def classifyDataLR(data, classifyTrained,
                classifySurface, selectFeatures=('KUC', 10),scaling=True):
    return classifyData(data, classifyTrained,
                    classifySurface, LRClassifier, selectFeatures,scaling)


class Classifier(object):
    '''
    classdocs
    '''
    def __init__(self, samples, featureNames,
                 classifications, classificationNames):
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
        self.getClf().fit(self.getSamples(), self.getClassifications())

    def predict(self, sample):
        p = self.getClf().predict(sample)
        return self.classNames[0+p]

    def score(self, samples, classifications):
        return self.getClf().score(samples, classifications)

    def crossValidation(self):
        scores = cross_validation.cross_val_score(self.getClf(),
                                self.getSamples(), self.getClassifications())
        print("Accuracy: \n mean:%f \n std:%f" % (scores.mean(), scores.std()))

    def showProperties(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def getFeatureNames(self):
        return self.featureNames
    
    @staticmethod     
    def getEstimator():
        raise NotImplementedError("Subclass must implement abstract method")

    def plotDecisionSurface(self):
        classifierClass = self.__class__
        [samples, featureNames] = selectFeatures(self.samples,
            self.classifications, self.featureNames,
            classifierClass, ('KUC', 2),silent=True)
        clf = classifierClass(samples,
            featureNames, self.classifications, self.classNames)

        X = samples
        if (type(X) != np.ndarray):
            X = X.toarray()
        Y = self.classifications
        h = 0.01

        xas = X[:, 0]
        yas = X[:, 1]

        x_min, x_max = min(xas) - 1, max(xas) + 1
        y_min, y_max = min(yas) - 1, max(yas) + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))

        Z = clf.getClf().predict(np.c_[xx.ravel(), yy.ravel()])

        Z = Z.reshape(xx.shape)

        ttl = (self.classifierName() + "  " + featureNames[0]
               + " - " + featureNames[1])

        cols = pl.cm.Paired
        fig = pl.figure()
        ax = fig.add_subplot(111, title=ttl)
        ax.contourf(xx, yy, Z, cmap=cols)
        ax.axis('off')
        ax.scatter(xas, yas, c=Y, cmap=cols)

        self.fit()

    def classifierName(self):
        return "undefined"
        
    def setTransformOperators(self,imputer,scaler):
        self.scaler = scaler
        self.imputer = imputer
        
    def extractData(self,X,scaling=False):
        return extractData(X, self.samples, self.scaler, self.featureNames,scaling)

class SVMClassifier(Classifier):

    def __init__(self, samples, featureNames, classifications,
                 classificationNames):
        self.clf = svm.SVC(kernel = 'linear', C = 0.8)
        Classifier.__init__(self, samples, featureNames,
                            classifications, classificationNames)

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
        for i, fa in enumerate(svArray):
            if (i < len(self.classNames)):
                print(self.classNames[i] + ":")
                bestFeatures = heapq.nlargest(5, enumerate(fa),
                                              operator.itemgetter(1))
                bestFeatures = [self.featureNames[x]
                                for x in zip(*bestFeatures)[0]]
                for f in bestFeatures:
                    print("  " + f)

    @staticmethod
    def getEstimator():
        return svm.SVC(kernel='linear')

    def classifierName(self):
        return "SVM"


class DTClassifier(Classifier):

    def __init__(self, samples, featureNames,
                 classifications, classificationNames):
        self.clf = tree.DecisionTreeClassifier(min_samples_split=8,
                                               max_depth=4)
        if (type(samples) == sprs.csr_matrix):
            samples = samples.toarray()
        Classifier.__init__(self, samples, featureNames,
                            classifications, classificationNames)

    def getClf(self):
        return self.clf

    def showFeatureImportances(self):
        featureArray = self.getClf().feature_importances_
        print("Feature importance:")
        for i, feature in enumerate(featureArray):
            if (feature != 0):
                print(" %s:\t%f" % (self.featureNames[i], feature))

    def createTreePdf(self):
        try:
            import pydot
        except:
            return
        dot_data = StringIO()
        tree.export_graphviz(self.getClf(),
                out_file = dot_data, feature_names = self.featureNames)
        graph = pydot.graph_from_dot_data(dot_data.getvalue())
        graph.write_pdf("DT" + "-".join(self.classNames) + ".pdf")

    def classifierName(self):
        return "DT"


class KNNClassifier(Classifier):
    def __init__(self, samples, featureNames,
                 classifications, classificationNames, k=10):
        self.clf = KNeighborsClassifier(n_neighbors=k, weights='distance')
        Classifier.__init__(self, samples,
                    featureNames, classifications, classificationNames)

    def getClf(self):   
        return self.clf

    def showKNeighborsGraph(self):
        graph = self.getClf().kneighbors_graph(self.samples)
        graph = graph.todense()
        cmap = colors.ListedColormap(['white', 'black'])
        fig = pl.figure()
        ax = fig.add_subplot(111, title="KNN: nearest neighbours graph")
        ax.imshow(graph, cmap)

    def classifierName(self):
        return "KNN"


class LRClassifier(Classifier):
    def __init__(self, samples, featureNames,
                 classifications, classificationNames):
        self.clf = LogisticRegression()
        Classifier.__init__(self, samples, featureNames,
                            classifications, classificationNames)

    def getClf(self):
        return self.clf

    def classifierName(self):
        return "LogReg"

    @staticmethod
    def getEstimator():
        return LogisticRegression()

if __name__ == '__main__':
    iris = datasets.load_iris()
    clf = SVMClassifier(iris.data,
                        ["sep len", "sep wdt", "pet len", "pet wdt"],
                        iris.target, ["Setosa", "Versicolour", "Virginica"])
    clf.plotDecisionSurface()
    pl.show()
