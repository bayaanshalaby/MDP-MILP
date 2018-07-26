import numpy as np
import matplotlib.pyplot as plt

class DiscreteVariablePlot:
    
    def __init__(self, name, samples):
        self.name = name 
        self.samples = np.asarray(samples)
        self.avgs = list()
        
    def addAvg(self, discreteVars):
        self.avgs.append(np.mean(discreteVars))
        
    def plot(self, colour):
        plt.title(self.name + " Average")
        plt.xlabel('Number of Samples (n)')
        plt.ylabel(self.name)
        y = np.asarray(self.avgs)
        plt.plot(self.samples, y, colour)   
        plt.grid()
        plt.show()