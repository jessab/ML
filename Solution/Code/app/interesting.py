'''
Created on 8-dec.-2013

@author: jessa
'''

import matplotlib.pyplot as plt
import tools.Tools as tls



def failingPeaks(path):
    from DataLoader import getData
    
    data = getData(path, None, True)
    
    samples = tls.getDictArray(data.Features)
    
    people = dict()
    peaks = dict()
    
    i=0
    for sample in samples:
        for f in sample.keys():
            countedPeaks = []
            if sample[f] is None:
                peak =  f.split('.')[1]
                countedPeaks+=peak
                if `i` in people:
                    people[`i`]+=1
                else:
                    people[`i`]=1
                    
                if f in peaks:
                    peaks[peak]+=1
                else:
                    peaks[peak]=1
        i+=1
                    
    print(people)
    print(peaks)
    print(len(people))
    print(len(peaks))
                
            
                    











def peakInfluenceTrained(peaksType):
    from tools.Tools import getDictArray
    import app.featuresMain as fm
    
    data = fm.main()
    trained = data.Trained.values
    features = getDictArray(data.Features)

    def plot(name):
        y = [v[peaksType+'.' + name] for v in features]
        fig, ax = plt.subplots()
        ax.scatter(trained,y)
        fig.tight_layout()
        ax.set_title("trained: "+ name)
        
    plot('varDist')
    plot('varPeak')
    plot('maxPeak')
    plot('maxDist')
    plot('minPeak')
    plot('minDist')
    plot('avPeak')
    plot('avDist')
    
    plt.show()
    
# Helaas praktisch geen effect :(
def peakInfluenceSurface(peaksType):
    from tools.Tools import getDictArray
    import app.featuresMain as fm
    
    data = fm.main()
    surface = data.Surface.values
    
    def surfaceToInt(surface):
        if 'Woodchip' in surface:
            return 0
        if 'Asphalt' in surface:
            return 1
        if 'Track' in surface:
            return 2
        
    surface = map(surfaceToInt,surface)
        
    
    features = getDictArray(data.Features)

    def plot(name):
        y = [v[peaksType+'.' + name] for v in features]
        fig, ax = plt.subplots()
        ax.scatter(surface,y)
        fig.tight_layout()
        ax.set_title("surface: "+ name)
        
    plot('varDist')
    plot('varPeak')
    plot('maxPeak')
    plot('maxDist')
    plot('minPeak')
    plot('minDist')
    plot('avPeak')
    plot('avDist')
    
if __name__ == '__main__':
    peakInfluenceSurface('ankle.cwt_hilbert_ncor')
    plt.show()