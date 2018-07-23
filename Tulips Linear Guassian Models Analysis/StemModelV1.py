from gurobipy import *
import numpy as np

class StemModel:
    def __init__(self, name, randomSeed, n):
        self.name = name
        self.randomSeed = randomSeed
        self.n = int(n)
        self.model = Model(self.name)
        self.buildModel()
    
    def buildModel(self):
        self.model.setParam('OutputFlag', 0)
        
        # Create Variables 
        tulip_type = self.model.addVar(vtype = GRB.BINARY, name = "Tulip Type")
        water = self.model.addVar(lb = 250, ub = 1000, name = "Amount of Water/week (mL)")
        avg = self.model.addVar(name = "Average")
        stdev = self.model.addVar(name = "Standard Deviation")
        
        # Set Objective
        i = 0
        np.random.seed(self.randomSeed)
        obj = LinExpr()
        
        while i < self.n:
            obj += avg + stdev*np.random.standard_normal()
            i += 1
            
        self.model.setObjective((1/self.n)*obj, GRB.MAXIMIZE)
        
        # Set constraints 
        M = 1000
        
        # Stem average constraints 
        self.model.addConstr(avg <= 15 + 0.0011*water + M*(1 - tulip_type))
        self.model.addConstr(avg >= 15 + 0.0011*water - M*(1 - tulip_type))
        self.model.addConstr(avg <= 15 + 0.001*water + M*tulip_type)
        self.model.addConstr(avg >= 15 + 0.001*water - M*tulip_type)

        # If tulip_type = 1, stdev = 5 + 0.01*water, else avg = 10 - 0.01*water
        self.model.addConstr(stdev <= 5 - 0.001*water + M*(1 - tulip_type))
        self.model.addConstr(stdev >= 5 - 0.001*water - M*(1 - tulip_type))
        self.model.addConstr(stdev <= 10 - 0.005*water + M*tulip_type)
        self.model.addConstr(stdev >= 10 - 0.005*water - M*tulip_type)

        #Budget Constraint
        self.model.addConstr(1.5*tulip_type + 1.0*(1 - tulip_type) + 0.015*water <= 12)

        # Optimize model
        self.model.optimize()
    
    def getVar(self, varName):
        return self.model.getVarByName(varName).x
    
    def getObj(self):
        return self.model.objVal
    
    def getSampleReward(self, trials):
        avgReward = 0
        i = 0
        while i < trials:
            avgReward += np.random.normal(self.getVar("Average"), self.getVar("Standard Deviation"))
            i += 1
        return avgReward/trials