from gurobipy import *
import numpy as np
import matplotlib.pyplot as plt
from StemFlowerModelV1 import StemFlowerModel

TulipTypeAvg = list()
AmountOfWaterAvg = list()
AmountOfWaterStdev = list()
OutdoorAvg = list()
ObjectiveValueAvg = list()
ObjectiveValueStdev = list()
SampleRewardAvg = list()
SampleRewardStdev = list()
    
def generateStemFlowerModels(samples, trials):
    for n in samples:
        TulipType = list()
        Water = list()
        Outdoor = list()
        Obj = list()
        Reward = list()
        i = 0
        while i < trials:
            name = "Model 2 at i = " + str(i) + " and n = " + str(n)
            sampleModel = StemFlowerModel(name, np.random.randint(10e6), n)
            TulipType.append(sampleModel.getVar("Tulip Type"))
            Water.append(sampleModel.getVar("Amount of Water/week (mL)"))
            Outdoor.append(sampleModel.getVar("Outdoor?"))
            Obj.append(sampleModel.getObj())
            Reward.append(sampleModel.getSampleReward(trials))
            i += 1
        TulipTypeAvg.append(np.mean(TulipType))
        AmountOfWaterAvg.append(np.mean(Water))
        AmountOfWaterStdev.append(np.std(Water))
        OutdoorAvg.append(np.mean(Outdoor))
        ObjectiveValueAvg.append(np.mean(Obj))
        ObjectiveValueStdev.append(np.std(Obj))
        SampleRewardAvg.append(np.mean(Reward))
        SampleRewardStdev.append(np.std(Reward))
        print("Generated " + str(trials) +  " Stem Flower Models for n = " + str(n))
    print("Completed generating all Stem Flower Models.")
    
def plotStemFlowerActions(samples, TulipTypeColour, WaterColour, WaterFill, OutdoorColour):
    fig, (TulipType, Water, Outdoors) = plt.subplots(1,3, figsize = (20, 5), sharey = False, sharex = True)

    # Tulip Type
    y = np.asarray(TulipTypeAvg)
    TulipType.set_title('Tulip Type Decision(1 = red, 0 = purple)')
    TulipType.set_xlabel('Number of Samples (n)')
    TulipType.set_ylabel('Tulip Type Decision')
    TulipType.plot(samples, y, TulipTypeColour)    
    TulipType.grid()

    # Amount of Water
    y = np.asarray(AmountOfWaterAvg)
    error = np.asarray(AmountOfWaterStdev)
    Water.set_title('Amount of Water/week (mL)')
    Water.set_xlabel('Number of Samples (n)')
    Water.set_ylabel('Amount of Water/week (mL)')
    Water.plot(samples, y, WaterColour)    
    Water.fill_between(samples, y - error, y + error, facecolor=WaterFill)
    Water.grid()

    # Outdoors
    y = np.asarray(OutdoorAvg)
    Outdoors.set_title('Outdoor (1 = yes, 0 = no)')
    Outdoors.set_xlabel('Number of Samples (n)')
    Outdoors.set_ylabel('Outdoor Decision')
    Outdoors.plot(samples, y, OutdoorColour)    
    Outdoors.grid()
    
def plotStemFlowerObjAndReward(samples, ObjColour, ObjFill, RewardColour, RewardFill):
    fig, (ObjectiveValue, SampleReward) = plt.subplots(1,2, figsize = (15, 5), sharey = False, sharex = True)

    # Objective Function Value
    y = np.asarray(ObjectiveValueAvg)
    error = np.asarray(ObjectiveValueStdev)
    ObjectiveValue.set_title('Objective Function Value')
    ObjectiveValue.set_xlabel('Number of Samples (n)')
    ObjectiveValue.set_ylabel('Objective Function Value')
    ObjectiveValue.set_ylim(22, 26)
    ObjectiveValue.plot(samples, y, ObjColour)  
    ObjectiveValue.fill_between(samples, y - error, y + error, facecolor= ObjFill)
    ObjectiveValue.grid()

    # Sample Reward
    y = np.asarray(SampleRewardAvg)
    error = np.asarray(SampleRewardStdev)
    SampleReward.set_title('Sampled Reward')
    SampleReward.set_xlabel('Number of Samples (n)')
    SampleReward.set_ylabel('SampledReward')
    SampleReward.set_ylim(22, 26)
    SampleReward.plot(samples, y, RewardColour)    
    SampleReward.fill_between(samples, y - error, y + error, facecolor=RewardFill)
    SampleReward.grid()
