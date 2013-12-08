'''
Created on 8-dec.-2013

@author: jessa
'''

def peakInfluenceTrained():
    from tools.Tools import getDictArray
    import app.featuresMain as fm
    import matplotlib.pyplot as plt
    
    data = fm.main()
    trained = data.Trained.values
    features = getDictArray(data.Features)

    def plot(name):
        y = [v['default.' + name] for v in features]
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
def peakInfluenceSurface():
    from tools.Tools import getDictArray
    import app.featuresMain as fm
    import matplotlib.pyplot as plt
    
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
        y = [v['default.' + name] for v in features]
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
    
    plt.show()
    
if __name__ == '__main__':
    peakInfluenceSurface()
    peakInfluenceTrained()