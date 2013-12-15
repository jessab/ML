'''
Created on 13-dec.-2013

@author: jessa
'''

import sys


def interpretInput(args):
    method = args[1]

    if method == 'classify':
        if len(args) < 4:
            print('not enough arguments')
            raise SystemExit(0)
        anklePath = args[2]
        hipPath = args[3]
        options = interpretClassifyOptions(anklePath, hipPath, args[4:])
        return (True, (anklePath, hipPath, options))

    elif method == 'experiment':
        options = interpretExperimentOptions(args[2:])
        return (False, options)


def interpretClassifyOptions(options):
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

    return lookForNextOptions(options, posOptions, defaultVals)


def interpretExperimentOptions(options):
    posOptions = {
            '-p': setPath,
            '-f': setFeatures
            }

    defaultVals = {
            'p': None,
            'f': 'all'
            }

    return lookForNextOptions(options, posOptions, defaultVals)


def lookForNextOptions(options, posOptions, vals):
    if len(options) == 0:
        return vals
    opt = options[0]
    if not opt in posOptions:
        print('unexpected input: ' + opt + ' is not a possible option')
        raise SystemExit(0)

    return posOptions[opt](options[1:], posOptions, vals)


def setClassifier(options, posOptions, vals):
    posClassifiers = ['trained', 'surface', 'combined']
    c = options[0]
    if c not in posClassifiers:
        print('classifier was expected')
        raise SystemExit(0)
    vals['c'] = c
    return lookForNextOptions(options, posOptions, vals)


def setAlgo(options, posOptions, vals):
    posAlgos = ['SVM', 'DT', 'KNN', 'LogReg']
    algo = options[0]
    if algo not in posAlgos:
        print('classification algorithm was expected')
        raise SystemExit(0)
    vals['a'] = algo
    return lookForNextOptions(options, posOptions, vals)


def setFeatures(options, posOptions, vals):
    posFeatures = ['all', 'K', 'KUC', 'RFECV']
    f = options[0]
    if f not in posFeatures:
        print('feature specification was expected')
        raise SystemExit(0)
    if f == 'all' or f == 'RFECV':
        vals['f'] = f
        return lookForNextOptions(options[1:], posOptions, vals)
    try:
        n = int(options[1])
    except:
        print("number of wanted features was not given")
        raise SystemExit(0)
    vals['f'] = (f, n)
    return lookForNextOptions(options[2:], posOptions, vals)


def setPath(options, posOptions, vals):
    vals['p'] = options[0]
    return lookForNextOptions(options[1:], posOptions, vals)

if __name__ == '__main__':
    print(interpretInput(sys.argv))
