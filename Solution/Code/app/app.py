'''
Created on 13-dec.-2013

@author: jessa
'''

import sys

import classification.ClassifyMain as cm
import featuresMain as fm
from dataTransform.Preprocessing import filterRun3
from dataTransform.accproc import preprocessGCDC, readGCDCFormat
from features.FeatureExtraction import extract
from inputInterpreter import interpretInput


def main(args):
    print(args[0])
    classification, arguments = interpretInput(args)

    if classification:
        anklePath, hipPath, options = arguments
        classify(anklePath, hipPath, options)

    else:
        experiment(arguments)


def classify(anklePath, hipPath, options):
    print("---- Classification ---- \n")
    print("Calculating features...")
    features = getFeatures(anklePath, hipPath)
    print("Predicting classification...")
    data = fm.main(True, options['p'])
    result = cm.predict(data, features,
                        options['a'], options['c'], options['f'])
    print(result)


def experiment(options):
    data = fm.main(True, options['p'])
    cm.main(data, options['f'])


def getFeatures(anklePath, hipPath):
    def getRunningPart(data, hip):
        try:
            return filterRun3(data, hip)
        except:
            return None

    def obtainFeatures(ankleData, hipData, features):
        try:
            return extract(ankleData, hipData, features)
        except:
            return None

    def getDataForOneBodyPart(path, hip):
        data = readGCDCFormat(path)
        data = preprocessGCDC(data)
        data = getRunningPart(data, hip)
        return data

    ankleData = getDataForOneBodyPart(anklePath, False)
    hipData = getDataForOneBodyPart(hipPath, True)

    return extract(ankleData, hipData, None)


if __name__ == '__main__':
    main(sys.argv)
