'''
Created on 8-dec.-2013

@author: jessa
'''

def peakInfluence():
    from tools.Tools import getDictArray
    import app.featuresMain as fm
    import matplotlib.pyplot as plt
    
    data = fm.main()
    trained = data.Trained.values
    print(trained)
    features = getDictArray(data.Features)

    def plot(name):
        y = [v['default.' + name] for v in features]
        fig, ax = plt.subplots()
        ax.scatter(trained,y)
        fig.tight_layout()
        ax.set_title(name)
        
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
    peakInfluence()