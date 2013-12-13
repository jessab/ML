'''
Created on 13-dec.-2013

@author: jessa
'''

import sys


def classify(anklePath, hipPath, options):
    posOptions = {
            '-c': setClassifier,
            '-a': setAlgo,
            '-f': setFeatures,
            '-p': setPath
            }

    defaultVals = {
            'c': ['all'],
            'a': ['all'],
            'f': 'all',
            'p': None
            }

    vals = lookForNextOptions(options, posOptions, defaultVals)
    print(vals)


def experiment(options):
    posOptions = {
            '-p': setPath,
            '-f': setFeatures
            }

    defaultVals = {
            'p': None,
            'f': 'all'
            }

    vals = lookForNextOptions(options, posOptions, defaultVals)
    print(vals)


def lookForNextOptions(options, posOptions, vals):
    if len(options) == 0:
        return vals
    opt = options[0]
    if not opt in posOptions:
        print('unexpected input: ' + opt + ' is not a possible option')
        raise Exception()

    return posOptions[opt](options[1:], posOptions, vals)


def setClassifier(options, posOptions, vals):
    posClassifiers = ['trained', 'surface', 'combo', 'all']
    classifiers = []
    for i in range(len(options)):
        c = options[i]
        if c in posClassifiers and not c in classifiers:
            classifiers.append(c)
        elif c in posOptions:
            if i == 0:
                print('no classifiers were added')
                raise Exception()
            vals['c'] = classifiers
            return lookForNextOptions(options[i:], posOptions, vals)
        else:
            print('confusing input. Don\'t know what to do with ' + options[i])
            raise Exception()


def setAlgo(options, posOptions, vals):
    posAlgos = ['svm', 'dt', 'knn', 'lr', 'all']
    algos = []
    for i in range(len(options)):
        a = options[i]
        if a in posAlgos and not a in algos:
            algos.append(a)
        elif a in posOptions:
            if i == 0:
                print('no classification algorithms were added')
                raise Exception()
            vals['a'] = algos
            return lookForNextOptions(options[i:], posOptions, vals)
        else:
            print('confusing input. Don\'t know what to do with ' + options[i])
            raise Exception()


def setFeatures(options, posOptions, vals):
    posFeatures = ['all', 'K', 'KUC']
    f = options[0]
    if f not in posFeatures:
        print('feature specification was expected')
        raise Exception()
    if f == 'all':
        vals['f'] = f
        return lookForNextOptions(options[1:], posOptions, vals)
    try:
        n = int(options[1])
    except:
        print("number of wanted features was not given")
        raise Exception()
    vals['f'] = (f, n)
    return lookForNextOptions(options[2:], posOptions, vals)


def setPath(options, posOptions, vals):
    vals['p'] = options[0]
    return lookForNextOptions(options[1:], posOptions, vals)

if __name__ == '__main__':
    args = sys.argv
    method = args[1]

    if method == 'classify':
        if len(args) < 4:
            print('not enough arguments')
            raise Exception()
        anklePath = args[2]
        hipPath = args[3]
        options = args[4:]
        classify(anklePath, hipPath, options)

    elif method == 'experiment':
        experiment(args[2:])
