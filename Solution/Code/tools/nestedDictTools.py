'''
Created on 11-dec.-2013

@author: jessa
'''
#### intersection ####


def intersection(v1, v2):
    try:
        return dict((k, intersection(v1[k], v2[k]))
                    for k in v1.keys() if k in v2.keys())
    except:
        return [l for l in v1 if l in v2]

#### difference ####


def diff(v1, v2):
# return everything from v1 which is not in v2
    try:
        return dict((k, diff(v1[k], v2[k])) for k in v1.keys())
    except:
        return [l for l in v1 if l not in v2]


#### union ####

def union(v1, v2):
# return everything from v1 which is not in v2
    try:
        return dict((k, union(v1[k], v2[k]))
                    for k in union(v1.keys(), v2.keys()))
    except:
        return v1 + [l for l in v2 if l not in v1]


#### empty ####

def isEmpty(d):
    try:
        return False not in (dict((k, isEmpty(d[k])) for k in d)).values()
    except:
        return len(d) == 0


#### exchange features and cols ###


def colsFirstFeaturesSecond(v1, v2):
    v3 = dict()
    for bodypart in v1.keys():
        v3[bodypart] = dict()
        for cat in v1[bodypart].keys():
            v3[bodypart][cat] = {
                                'cols': v1[bodypart][cat]['cols'],
                                'features': v2[bodypart][cat]['features']
                               }
    return v3


if __name__ == '__main__':
    from features.featuresToRequiredDict import featuresToRequiredDict

    l1 = {'a': ['a', 'b', 'c', 'd']}
    l2 = {'a': ['c', 'd', 'e', 'f']}

    print(union(l1, l2))
    print(union([1, 2, 3], [3, 4, 5]))

    features1 = ['hip.Ax.min', 'ankle.AyAz.fcovar'
                  'hip.Vx.av', 'ankle.simple_nosmooth.maxDist',
                  'hip.cwt_butter_ncor.avPeak', 'ankle.cwt_butter_cor.maxDist',
                  'head.fout.ief']
    dict1 = featuresToRequiredDict(features1)
    features2 = []
    dict2 = featuresToRequiredDict(features2)

    print(dict1)
    print(dict2)
    ex1 = colsFirstFeaturesSecond(dict1, dict2)
    print(ex1)
