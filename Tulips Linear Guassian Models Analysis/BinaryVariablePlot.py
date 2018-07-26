import numpy as np
import matplotlib.pyplot as plt

class BinaryVariablePlot:
    
    def __init__(self, name, samples):
        self.name = name 
        self.samples = np.asarray(samples)
        self.ratios = list()

    def addRatio(self, binaryVars):
        pos = binaryVars.count(0.0)
        tot = len(binaryVars)
        self.ratios.append(pos/tot)
        
    def plot(self, colour):
        plt.title(self.name + " Confidence Ratio")
        plt.xlabel('Number of Samples (n)')
        plt.ylabel(self.name)
        y = np.asarray(self.ratios)
        plt.plot(self.samples, y, colour)   
        plt.grid()
        plt.show()