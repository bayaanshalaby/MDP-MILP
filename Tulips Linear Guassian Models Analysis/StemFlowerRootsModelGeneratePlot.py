from gurobipy import *
import numpy as np
import matplotlib.pyplot as plt
from StemFlowerRootsModelV1 import StemFlowerRootsModel

TulipTypeAvg = list()
AmountOfWaterAvg = list()
AmountOfWaterStdev = list()
OutdoorAvg = list()
PelletsAvg = list()
ObjectiveValueAvg = list()
ObjectiveValueStdev = list()
SampleRewardAvg = list()
SampleRewardStdev = list()

def generateStemFlowerRootsModels(samples, trials):
    for n in samples:
        TulipType = list()
        Water = list()
        Outdoor = list()
        Pellets = list()
        Obj = list()
        Reward = list()
        i = 0
        while i < trials:
            name = "Model 2 at i = " + str(i) + " and n = " + str(n)
            sampleModel = StemFlowerRootsModel(name, np.random.randint(10e6), n)
            TulipType.append(sampleModel.getVar("Tulip Type"))
            Water.append(sampleModel.getVar("Amount of Water/week (mL)"))
            Outdoor.append(sampleModel.getVar("Outdoor?"))
            Pellets.append(sampleModel.getVar("Number of Fertilizer Pellets"))
            Obj.append(sampleModel.getObj())
            Reward.append(sampleModel.getSampleReward(trials))
            i += 1
        TulipTypeAvg.append(np.mean(TulipType))
        AmountOfWaterAvg.append(np.mean(Water))
        AmountOfWaterStdev.append(np.std(Water))
        OutdoorAvg.append(np.mean(Outdoor))
        PelletsAvg.append(np.mean(Pellets))
        ObjectiveValueAvg.append(np.mean(Obj))
        ObjectiveValueStdev.append(np.std(Obj))
        SampleRewardAvg.append(np.mean(Reward))
        SampleRewardStdev.append(np.std(Reward))
        print("Generated " + str(trials) +  " Stem Flower Roots Models for n = " + str(n))
    print("Completed generating all Stem Flower Roots Models.")
    
def plotStemFlowerRootsActions(samples, TulipTypeColour, WaterColour, WaterFill, OutdoorColour, PelletsColour):
    fig1, (TulipType, Water) = plt.subplots(1,2, figsize = (15, 5), sharey = False, sharex = True)
    fig2, (Outdoors, Pellets) = plt.subplots(1,2, figsize = (15, 5), sharey = False, sharex = True)

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
                           
    # Pellets 
    y = np.asarray(PelletsAvg)
    Pellets.set_title('Number of Fertilizer Pellets')
    Pellets.set_xlabel('Number of Samples (n)')
    Pellets.set_ylabel('Number of Fertilizer Pellets')
    Pellets.plot(samples, y, PelletsColour)    
    Pellets.grid()
                           
def plotStemFlowerRootsObjAndReward(samples, ObjColour, ObjFill, RewardColour, RewardFill):
    fig, (ObjectiveValue, SampleReward) = plt.subplots(1,2, figsize = (15, 5), sharey = False, sharex = True)

    # Objective Function Value
    y = np.asarray(ObjectiveValueAvg)
    error = np.asarray(ObjectiveValueStdev)
    ObjectiveValue.set_title('Objective Function Value')
    ObjectiveValue.set_xlabel('Number of Samples (n)')
    ObjectiveValue.set_ylabel('Objective Function Value')
    ObjectiveValue.set_ylim(36, 43)
    ObjectiveValue.plot(samples, y, ObjColour)
    ObjectiveValue.fill_between(samples, y - error, y + error, facecolor= ObjFill)
    ObjectiveValue.grid()

    # Sample Reward
    y = np.asarray(SampleRewardAvg)
    error = np.asarray(SampleRewardStdev)
    SampleReward.set_title('Sampled Reward')
    SampleReward.set_xlabel('Number of Samples (n)')
    SampleReward.set_ylabel('SampledReward')
    SampleReward.set_ylim(36, 43)
    SampleReward.plot(samples, y, RewardColour)    
    SampleReward.fill_between(samples, y - error, y + error, facecolor=RewardFill)
    SampleReward.grid()