from gurobipy import *
import numpy as np

class StemModel:
    def __init__(self, name, randomSeed, n):
        self.name = name
        self.randomSeed = randomSeed
        self.n = int(n)
        self.model = Model(self.name)
        self.redParams = {"Stem Base Avg" : 15, 
                          "Stem Water Ratio Avg" : 0.0012, 
                          "Stem Base Stdev" : 5,
                          "Stem Water Ratio Stdev" : - 0.001}
        self.purpleParams = {"Stem Base Avg" : 15, 
                             "Stem Water Ratio Avg" : 0.001, 
                             "Stem Base Stdev" : 10,
                             "Stem Water Ratio Stdev" : - 0.005}
        self.costParams = {"Red Tulip" : 1.5, 
                           "Purple Tulip": 1.0, 
                           "Water": 0.015}
        self.buildModel()
    
    def buildModel(self):
        self.model.setParam('OutputFlag', 0)
        
        # Create Variables 
        tulip_type = self.model.addVar(vtype = GRB.BINARY, name = "Tulip Type")
        water = self.model.addVar(lb = 250, ub = 1000, name = "Amount of Water/week (mL)")
        avg = self.model.addVar(name = "Average")
        stdev = self.model.addVar(name = "Standard Deviation")
        
        # Set Objective
        np.random.seed(self.randomSeed)
        norms = np.random.standard_normal(self.n)
        self.navg = np.mean(norms)
        self.model.setObjective((1/self.n)*(sum(avg + stdev*norm for norm in norms)), GRB.MAXIMIZE)

        # Set constraints 
        M = 1000
        
        # Stem average constraints 
        self.model.addConstr(avg <= self.redParams.get("Stem Base Avg") 
                             + self.redParams.get("Stem Water Ratio Avg")*water + M*(1 - tulip_type))
        self.model.addConstr(avg >= self.redParams.get("Stem Base Avg") 
                             + self.redParams.get("Stem Water Ratio Avg")*water - M*(1 - tulip_type))
        self.model.addConstr(avg <= self.purpleParams.get("Stem Base Avg") 
                             + self.purpleParams.get("Stem Water Ratio Avg")*water + M*tulip_type)
        self.model.addConstr(avg >= self.purpleParams.get("Stem Base Avg") 
                             + self.purpleParams.get("Stem Water Ratio Avg")*water - M*tulip_type)

        # Stem standard deviation 
        self.model.addConstr(stdev <= self.redParams.get("Stem Base Stdev") 
                             + self.redParams.get("Stem Water Ratio Stdev")*water + M*(1 - tulip_type))
        self.model.addConstr(stdev >= self.redParams.get("Stem Base Stdev") 
                             + self.redParams.get("Stem Water Ratio Stdev")*water - M*(1 - tulip_type))
        self.model.addConstr(stdev <= self.purpleParams.get("Stem Base Stdev") 
                             + self.purpleParams.get("Stem Water Ratio Stdev")*water + M*tulip_type)
        self.model.addConstr(stdev >= self.purpleParams.get("Stem Base Stdev") 
                             + self.purpleParams.get("Stem Water Ratio Stdev")*water - M*tulip_type)

        #Budget Constraint
        self.model.addConstr(self.costParams.get("Red Tulip")*tulip_type
                             + self.costParams.get("Purple Tulip")*(1 - tulip_type) 
                             + self.costParams.get("Water")*water <= 12)
        
        # Optimize Model
        self.model.optimize()
        
    def setRedParam(self, name, value):
        self.redParams.setDefaultValue(name, value)
        
    def setPurpleParam(self, name, value):
        self.purpleParams.setDefaultValue(name, value)
        
    def setCostParam(self, name, value):
        self.costParams.setDefaultValue(name, value)
    
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
    
    def testResults(self):
        if self.getVar("Tulip Type") == 1:
            checkAvg = self.redParams.get("Stem Base Avg") + self.redParams.get("Stem Water Ratio Avg")*self.getVar("Amount of Water/week (mL)")
            checkStdev = self.redParams.get("Stem Base Stdev") + self.redParams.get("Stem Water Ratio Stdev")*self.getVar("Amount of Water/week (mL)")
        else:
            checkAvg = self.purpleParams.get("Stem Base Avg") + self.purpleParams.get("Stem Water Ratio Avg")*self.getVar("Amount of Water/week (mL)")
            checkStdev = self.purpleParams.get("Stem Base Stdev") + self.purpleParams.get("Stem Water Ratio Stdev")*self.getVar("Amount of Water/week (mL)")   
        for v in self.model.getVars():
            print('Gurobi Result: %s: %g' % (v.varName, v.x))
            if v.varName == "Average":
                print("\tCheck Result: " + str(checkAvg))
            elif v.varName == "Standard Deviation":
                print("\tCheck Result: " + str(checkStdev))
                
        print('Gurobi Stem Height: %g' % self.getObj())
        print("\tCheck Stem Height Result: " + str(checkAvg + checkStdev*self.navg))