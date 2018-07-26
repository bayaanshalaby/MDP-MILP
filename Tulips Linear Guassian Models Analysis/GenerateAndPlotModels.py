import numpy as np
from StemModelV1 import StemModel
from StemFlowerModelV1 import StemFlowerModel
from StemFlowerRootsModelV1 import StemFlowerRootsModel
from BinaryVariablePlot import BinaryVariablePlot
from DiscreteVariablePlot import DiscreteVariablePlot
from ContinuousVariablePlot import ContinuousVariablePlot

StemPlots = {}
StemFlowerPlots = {}
StemFlowerRootsPlots = {}

def generateStemModels(samples, trials):
    
    StemPlots.clear()
    StemPlots.setdefault("Tulip Type", BinaryVariablePlot("Tulip Type", samples))
    StemPlots.setdefault("Amount of Water", ContinuousVariablePlot("Amount of Water/week (mL)", samples))
    StemPlots.setdefault("Objective Function Value", ContinuousVariablePlot("Objective Function Value", samples))
    StemPlots.setdefault("Sampled Reward", ContinuousVariablePlot("Sampled Reward", samples))
    StemPlots.setdefault("Runtime", DiscreteVariablePlot("Total Runtime (s)", samples))
    StemPlots.setdefault("Optimization Time", DiscreteVariablePlot("Optimization Time (s)", samples))
    StemPlots.setdefault("Simplex Iterations", DiscreteVariablePlot("Number of Simplex Iterations", samples))
    
    for n in samples:
        
        TulipType = list()
        Water = list()
        Obj = list()
        Reward = list()
        Runtime = list()
        OptTime = list()
        SimplexIter = list()
        
        i = 0
        while i < trials:
            name = "Model 1 at i = " + str(i) + " and n = " + str(n)
            sampleModel = StemModel(name, np.random.randint(10e6), n)
            TulipType.append(sampleModel.getVar("Tulip Type"))
            Water.append(sampleModel.getVar("Amount of Water/week (mL)"))
            Obj.append(sampleModel.getObj())
            Reward.append(sampleModel.getSampleReward(trials))
            Runtime.append(sampleModel.getRunTime())
            OptTime.append(sampleModel.getOptimizationTime())
            SimplexIter.append(sampleModel.getSimplexIters())
            i += 1
            
        StemPlots.get("Tulip Type").addRatio(TulipType)
        StemPlots.get("Amount of Water").addAvgAndStdev(Water)
        StemPlots.get("Objective Function Value").addAvgAndStdev(Obj)
        StemPlots.get("Sampled Reward").addAvgAndStdev(Reward)
        StemPlots.get("Runtime").addAvg(Runtime)
        StemPlots.get("Optimization Time").addAvg(OptTime)
        StemPlots.get("Simplex Iterations").addAvg(SimplexIter)
        print("Generated " + str(trials) +  " Stem Models for n = " + str(n))
        
    print("Completed generating all Stem Models.")
    
def generateStemFlowerModels(samples, trials):
    
    StemFlowerPlots.clear()
    StemFlowerPlots.setdefault("Tulip Type", BinaryVariablePlot("Tulip Type", samples))
    StemFlowerPlots.setdefault("Amount of Water", ContinuousVariablePlot("Amount of Water/week (mL)", samples))
    StemFlowerPlots.setdefault("Outdoor", BinaryVariablePlot("Outdoors", samples))
    StemFlowerPlots.setdefault("Objective Function Value", ContinuousVariablePlot("Objective Function Value", samples))
    StemFlowerPlots.setdefault("Sampled Reward", ContinuousVariablePlot("Sampled Reward", samples))
    StemFlowerPlots.setdefault("Runtime", DiscreteVariablePlot("Total Runtime (s)", samples))
    StemFlowerPlots.setdefault("Optimization Time", DiscreteVariablePlot("Optimization Time (s)", samples))
    StemFlowerPlots.setdefault("Simplex Iterations", DiscreteVariablePlot("Number of Simplex Iterations", samples))
    
    for n in samples:
        
        TulipType = list()
        Water = list()
        Outdoor = list()
        Obj = list()
        Reward = list()
        Runtime = list()
        OptTime = list()
        SimplexIter = list()
        
        i = 0
        while i < trials:
            name = "Model 2 at i = " + str(i) + " and n = " + str(n)
            sampleModel = StemFlowerModel(name, np.random.randint(10e6), n)
            TulipType.append(sampleModel.getVar("Tulip Type"))
            Water.append(sampleModel.getVar("Amount of Water/week (mL)"))
            Outdoor.append(sampleModel.getVar("Outdoor?"))
            Obj.append(sampleModel.getObj())
            Reward.append(sampleModel.getSampleReward(trials))
            Runtime.append(sampleModel.getRunTime())
            OptTime.append(sampleModel.getOptimizationTime())
            SimplexIter.append(sampleModel.getSimplexIters())
            i += 1
            
        StemFlowerPlots.get("Tulip Type").addRatio(TulipType)
        StemFlowerPlots.get("Amount of Water").addAvgAndStdev(Water)
        StemFlowerPlots.get("Outdoor").addRatio(Outdoor)
        StemFlowerPlots.get("Objective Function Value").addAvgAndStdev(Obj)
        StemFlowerPlots.get("Sampled Reward").addAvgAndStdev(Reward)
        StemFlowerPlots.get("Runtime").addAvg(Runtime)
        StemFlowerPlots.get("Optimization Time").addAvg(OptTime)
        StemFlowerPlots.get("Simplex Iterations").addAvg(SimplexIter)
        print("Generated " + str(trials) +  " Stem Flower Models for n = " + str(n))
        
    print("Completed generating all Stem Flower Models.")

def generateStemFlowerRootsModels(samples, trials):
    
    StemFlowerRootsPlots.clear()
    StemFlowerRootsPlots.setdefault("Tulip Type", BinaryVariablePlot("Tulip Type", samples))
    StemFlowerRootsPlots.setdefault("Amount of Water", ContinuousVariablePlot("Amount of Water/week (mL)", samples))
    StemFlowerRootsPlots.setdefault("Outdoor", BinaryVariablePlot("Outdoors", samples))
    StemFlowerRootsPlots.setdefault("Pellets", DiscreteVariablePlot("Number of Fertilizer Pellets/week", samples))
    StemFlowerRootsPlots.setdefault("Objective Function Value", ContinuousVariablePlot("Objective Function Value", samples))
    StemFlowerRootsPlots.setdefault("Sampled Reward", ContinuousVariablePlot("Sampled Reward", samples))
    StemFlowerRootsPlots.setdefault("Runtime", DiscreteVariablePlot("Total Runtime (s)", samples))
    StemFlowerRootsPlots.setdefault("Optimization Time", DiscreteVariablePlot("Optimization Time (s)", samples))
    StemFlowerRootsPlots.setdefault("Simplex Iterations", DiscreteVariablePlot("Number of Simplex Iterations", samples))
    
    for n in samples:
        
        TulipType = list()
        Water = list()
        Outdoor = list()
        Pellets = list()
        Obj = list()
        Reward = list()
        Runtime = list()
        OptTime = list()
        SimplexIter = list()
        
        i = 0
        while i < trials:
            name = "Model 3 at i = " + str(i) + " and n = " + str(n)
            sampleModel = StemFlowerRootsModel(name, np.random.randint(10e6), n)
            TulipType.append(sampleModel.getVar("Tulip Type"))
            Water.append(sampleModel.getVar("Amount of Water/week (mL)"))
            Outdoor.append(sampleModel.getVar("Outdoor?"))
            Pellets.append(sampleModel.getVar("Number of Fertilizer Pellets"))
            Obj.append(sampleModel.getObj())
            Reward.append(sampleModel.getSampleReward(trials))
            Runtime.append(sampleModel.getRunTime())
            OptTime.append(sampleModel.getOptimizationTime())
            SimplexIter.append(sampleModel.getSimplexIters())
            i += 1
            
        StemFlowerRootsPlots.get("Tulip Type").addRatio(TulipType)
        StemFlowerRootsPlots.get("Amount of Water").addAvgAndStdev(Water)
        StemFlowerRootsPlots.get("Outdoor").addRatio(Outdoor)
        StemFlowerRootsPlots.get("Pellets").addAvg(Pellets)
        StemFlowerRootsPlots.get("Objective Function Value").addAvgAndStdev(Obj)
        StemFlowerRootsPlots.get("Sampled Reward").addAvgAndStdev(Reward)
        StemFlowerRootsPlots.get("Runtime").addAvg(Runtime)
        StemFlowerRootsPlots.get("Optimization Time").addAvg(OptTime)
        StemFlowerRootsPlots.get("Simplex Iterations").addAvg(SimplexIter)  
        print("Generated " + str(trials) +  " Stem Flower Roots Models for n = " + str(n))
        
    print("Completed generating all Stem Flower Roots Models.")
    
def plotStemVariable(name, colour):
    StemPlots.get(name).plot(colour)

def plotStemFlowerVariable(name, colour):
    StemFlowerPlots.get(name).plot(colour)
    
def plotStemFlowerRootsVariable(name, colour):
    StemFlowerRootsPlots.get(name).plot(colour)