import numpy as np
import matplotlib.pyplot as plt

class ContinuousVariablePlot:
    
    def __init__(self, name, samples):
        self.name = name 
        self.samples = np.asarray(samples)
        self.avgs = list()
        self.stdevs = list()
        
    def addAvgAndStdev(self, continuousVars):
        self.avgs.append(np.mean(continuousVars))
        self.stdevs.append(np.std(continuousVars))
        
    def getFillColour(self, colour):
        if colour == 'b':
            return '#089FFF'
        elif colour == 'Purple':
            return '#FF9848'
        elif colour == 'g':
            return '#7EFF99'
        else:
            return '#D2D7DB'
        
    def plot(self, colour):
            fig, (avgAx, stdAx) = plt.subplots(1,2, figsize = (15, 5), sharey = False, sharex = True)
            y = np.asarray(self.avgs)
            error = np.asarray(self.stdevs)
            
            avgAx.set_title(self.name + " Average")
            avgAx.set_xlabel('Number of Samples (n)')
            avgAx.set_ylabel(self.name + " Average")
            avgAx.plot(self.samples, y, colour)  
            avgAx.fill_between(self.samples, y - error, y + error, facecolor= self.getFillColour(colour))
            avgAx.grid()
            
            stdAx.set_title(self.name + " Standard Deviation")
            stdAx.set_xlabel('Number of Samples (n)')
            stdAx.set_ylabel(self.name + " Standard Deviation")
            stdAx.plot(self.samples, error, colour)  
            stdAx.grid()