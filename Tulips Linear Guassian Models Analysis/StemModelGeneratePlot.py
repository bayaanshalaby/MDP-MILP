from gurobipy import *
import numpy as np
import matplotlib.pyplot as plt
from StemModelV2 import StemModel

TulipTypeAvg = list()
AmountOfWaterAvg = list()
AmountOfWaterStdev = list()
ObjectiveValueAvg = list()
ObjectiveValueStdev = list()
SampleRewardAvg = list()
SampleRewardStdev = list()

def generateStemModels(samples, trials):
    for n in samples:
        TulipType = list()
        Water = list()
        Obj = list()
        Reward = list()
        i = 0
        while i < trials:
            name = "Model 1 at i = " + str(i) + " and n = " + str(n)
            sampleModel = StemModel(name, np.random.randint(10e6), n)
            TulipType.append(sampleModel.getVar("Tulip Type"))
            Water.append(sampleModel.getVar("Amount of Water/week (mL)"))
            Obj.append(sampleModel.getObj())
            Reward.append(sampleModel.getSampleReward(trials))
            i += 1
        TulipTypeAvg.append(np.mean(TulipType))
        AmountOfWaterAvg.append(np.mean(Water))
        AmountOfWaterStdev.append(np.std(Water))
        ObjectiveValueAvg.append(np.mean(Obj))
        ObjectiveValueStdev.append(np.std(Obj))
        SampleRewardAvg.append(np.mean(Reward))
        SampleRewardStdev.append(np.std(Reward))
        print("Generated " + str(trials) +  " Stem Models for n = " + str(n))
    print("Completed generating all Stem Models.")
    
def plotStemActions(samples, TulipTypeColour, WaterColour, WaterFill):
    fig, (TulipType, Water) = plt.subplots(1,2, figsize = (15, 5), sharey = False, sharex = True)

    # Tulip Type
    y = np.asarray(TulipTypeAvg)
    TulipType.set_title('Tulip Type (1 = red, 0 = purple)')
    TulipType.set_xlabel('Number of Samples (n)')
    TulipType.set_ylabel('Tulip Type')
    TulipType.plot(samples, y, TulipTypeColour)    
    TulipType.grid()

    # Amount of Water
    y = np.asarray(AmountOfWaterAvg)
    error = np.asarray(AmountOfWaterStdev)
    Water.set_title('Amount of Water/week (mL)')
    Water.set_xlabel('Number of Samples (n)')
    Water.set_ylabel('Amount of Water/week (mL)')
    Water.plot(samples, y, WaterColour)    
    Water.fill_between(samples, y - error, y + error, facecolor= WaterFill)
    Water.grid()
    
def plotStemObjAndReward(samples, ObjColour, ObjFill, RewardColour, RewardFill):
    fig, (ObjectiveValue, SampleReward) = plt.subplots(1,2, figsize = (15, 5), sharey = False, sharex = True)

    # Objective Function Value
    y = np.asarray(ObjectiveValueAvg)
    error = np.asarray(ObjectiveValueStdev)
    ObjectiveValue.set_title('Objective Function Value')
    ObjectiveValue.set_xlabel('Number of Samples (n)')
    ObjectiveValue.set_ylabel('Objective Function Value')
    ObjectiveValue.set_ylim(14.0, 17.0)
    ObjectiveValue.plot(samples, y, ObjColour)  
    ObjectiveValue.fill_between(samples, y - error, y + error, facecolor= ObjFill)
    ObjectiveValue.grid()

    # Sample Reward
    y = np.asarray(SampleRewardAvg)
    error = np.asarray(SampleRewardStdev)
    SampleReward.set_title('Sampled Reward')
    SampleReward.set_xlabel('Number of Samples (n)')
    SampleReward.set_ylabel('SampledReward')
    SampleReward.set_ylim(14.0, 17.0)
    SampleReward.plot(samples, y, RewardColour)    
    SampleReward.fill_between(samples, y - error, y + error, facecolor=RewardFill)
    SampleReward.grid()