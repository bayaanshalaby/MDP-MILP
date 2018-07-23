from gurobipy import *
import numpy as np

class StemFlowerModel:
    def __init__(self, name, randomSeed, n):
        self.name = name
        self.randomSeed = randomSeed
        self.n = int(n)
        self.model = Model(self.name)
        self.redParams = {"Leaf Base Avg" : 131,
                          "Leaf Water Ratio Avg" : 0.05,
                          "Leaf Outdoor Ratio Avg" : 20,
                          "Leaf Base Stdev" : 65,
                          "Leaf Water Ratio Stdev": -0.001,
                          "Leaf Outdoor Ratio Stdev": 1,
                          "Flower Base Avg": 6,
                          "Flower Water Ratio Avg": -0.001,
                          "Flower Outdoor Ratio Avg": 2,
                          "Flower Base Stdev": 1.35,
                          "Flower Outdoor Ratio Stdev": 1}
        self.purpleParams = {"Leaf Base Avg" : 150,
                          "Leaf Water Ratio Avg" : 0.005,
                          "Leaf Outdoor Ratio Avg" : 5,
                          "Leaf Base Stdev" : 30,
                          "Leaf Water Ratio Stdev": -0.005,
                          "Leaf Outdoor Ratio Stdev": 1,
                          "Flower Base Avg": 8,
                          "Flower Water Ratio Avg": -0.0015,
                          "Flower Outdoor Ratio Avg": 1,
                          "Flower Base Stdev": 0.75,
                          "Flower Outdoor Ratio Stdev": 1}                  
        self.costParams = {"Red Tulip" : 1.5, 
                           "Purple Tulip": 1.0, 
                           "Water": 0.015,
                           "Outdoor": 2}
        self.buildModel()
    
    def buildModel(self):
        self.model.setParam('OutputFlag', 0)

        # Create Variables 
        tulip_type = self.model.addVar(vtype = GRB.BINARY, name = "Tulip Type")
        water = self.model.addVar(lb = 250, ub = 1000, name = "Amount of Water/week (mL)")
        outdoor = self.model.addVar(vtype = GRB.BINARY, name = "Outdoor?")
        lsaavg = self.model.addVar(name = "Total Leaf Surface Area Average")
        lsastdev = self.model.addVar(name = "Total Leaf Surface Area Standard Deviation")
        flavg = self.model.addVar(name = "Flower Petal Height Average")
        flstdev = self.model.addVar(name = "Flower Petal Height Standard Deviation")
        self.model.update()
        
        # Set objective 
        np.random.seed(self.randomSeed)
        lnorms = np.random.standard_normal(self.n)
        self.lavg = np.mean(lnorms)
        snorms = np.random.standard_normal(self.n)
        self.savg = np.mean(snorms)
        fnorms = np.random.standard_normal(self.n)
        self.favg = np.mean(fnorms)
        leaf = (1/self.n)*(sum(lsaavg + lsastdev*lnorm for lnorm in lnorms))
        stem = (1/self.n)*(sum(0.1*leaf + 0.05*leaf*snorm for snorm in snorms))
        flower = (1/self.n)*(sum(flavg + flstdev*fnorm for fnorm in fnorms))
        self.model.setObjective(stem + flower, GRB.MAXIMIZE)

        # Set constraints 
        M = 10000
        
        #Leaf Constraints     
        # Average constraints
        self.model.addConstr(lsaavg <= self.redParams.get("Leaf Base Avg") 
                             + self.redParams.get("Leaf Water Ratio Avg")*water 
                             + self.redParams.get("Leaf Outdoor Ratio Avg")*outdoor + M*(1 - tulip_type))
        self.model.addConstr(lsaavg >= self.redParams.get("Leaf Base Avg") 
                             + self.redParams.get("Leaf Water Ratio Avg")*water 
                             + self.redParams.get("Leaf Outdoor Ratio Avg")*outdoor - M*(1 - tulip_type))
        self.model.addConstr(lsaavg <= self.purpleParams.get("Leaf Base Avg") 
                             + self.purpleParams.get("Leaf Water Ratio Avg")*water 
                             + self.purpleParams.get("Leaf Outdoor Ratio Avg")*outdoor + M*tulip_type)
        self.model.addConstr(lsaavg >= self.purpleParams.get("Leaf Base Avg") 
                             + self.purpleParams.get("Leaf Water Ratio Avg")*water 
                             + self.purpleParams.get("Leaf Outdoor Ratio Avg")*outdoor - M*tulip_type)
        # Standard Deviation Constraints 
        self.model.addConstr(lsastdev <= self.redParams.get("Leaf Base Stdev") 
                             + self.redParams.get("Leaf Water Ratio Stdev")*water 
                             + self.redParams.get("Leaf Outdoor Ratio Stdev")*outdoor + M*(1 - tulip_type))
        self.model.addConstr(lsastdev >= self.redParams.get("Leaf Base Stdev") 
                             + self.redParams.get("Leaf Water Ratio Stdev")*water 
                             + self.redParams.get("Leaf Outdoor Ratio Stdev")*outdoor - M*(1 - tulip_type))
        self.model.addConstr(lsastdev <= self.purpleParams.get("Leaf Base Stdev") 
                             + self.purpleParams.get("Leaf Water Ratio Stdev")*water 
                             + self.purpleParams.get("Leaf Outdoor Ratio Stdev")*outdoor + M*tulip_type)
        self.model.addConstr(lsastdev >= self.purpleParams.get("Leaf Base Stdev") 
                             + self.purpleParams.get("Leaf Water Ratio Stdev")*water 
                             + self.purpleParams.get("Leaf Outdoor Ratio Stdev")*outdoor - M*tulip_type)
        
        # Flower Constraints 
        # Average Constraints 
        self.model.addConstr(flavg <= self.redParams.get("Flower Base Avg") 
                             + self.redParams.get("Flower Water Ratio Avg")*water 
                             + self.redParams.get("Flower Outdoor Ratio Avg")*outdoor + M*(1 - tulip_type))
        self.model.addConstr(flavg >= self.redParams.get("Flower Base Avg") 
                             + self.redParams.get("Flower Water Ratio Avg")*water 
                             + self.redParams.get("Flower Outdoor Ratio Avg")*outdoor - M*(1 - tulip_type))
        self.model.addConstr(flavg <= self.purpleParams.get("Flower Base Avg") 
                             + self.purpleParams.get("Flower Water Ratio Avg")*water 
                             + self.purpleParams.get("Flower Outdoor Ratio Avg")*outdoor + M*tulip_type)
        self.model.addConstr(flavg >= self.purpleParams.get("Flower Base Avg") 
                             + self.purpleParams.get("Flower Water Ratio Avg")*water 
                             + self.purpleParams.get("Flower Outdoor Ratio Avg")*outdoor - M*tulip_type)
        
        # Standard Deviation Constraints
        self.model.addConstr(flstdev <= self.redParams.get("Flower Base Stdev")
                             + self.redParams.get("Flower Outdoor Ratio Stdev")*outdoor + M*(1 - tulip_type))
        self.model.addConstr(flstdev >= self.redParams.get("Flower Base Stdev")
                             + self.redParams.get("Flower Outdoor Ratio Stdev")*outdoor - M*(1 - tulip_type))
        self.model.addConstr(flstdev <= self.purpleParams.get("Flower Base Stdev") 
                             + self.purpleParams.get("Flower Outdoor Ratio Stdev")*outdoor + M*tulip_type)
        self.model.addConstr(flstdev >= self.purpleParams.get("Flower Base Stdev")
                             + self.purpleParams.get("Flower Outdoor Ratio Stdev")*outdoor - M*tulip_type)
        
        #Budget Constraint
        self.model.addConstr(self.costParams.get("Red Tulip")*tulip_type
                             + self.costParams.get("Purple Tulip")*(1 - tulip_type) 
                             + self.costParams.get("Water")*water 
                             + self.costParams.get("Outdoor")*(1 - outdoor) <= 12)

        # Optimize model
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
        i = 0
        avgReward = 0
        while i < trials: 
            leafSA = np.random.normal(self.getVar("Total Leaf Surface Area Average"), self.getVar("Total Leaf Surface Area Standard Deviation"))
            while leafSA < 0:
                leafSA = np.random.normal(self.getVar("Total Leaf Surface Area Average"), self.getVar("Total Leaf Surface Area Standard Deviation"))
            stemHeight = np.random.normal(0.1*leafSA, 0.05*leafSA)
            flHeight = np.random.normal(self.getVar("Flower Petal Height Average"), self.getVar("Flower Petal Height Standard Deviation"))
            avgReward += stemHeight + flHeight 
            i += 1
        return avgReward/trials
    
    def testResults(self):
        if self.getVar("Tulip Type") == 1:
            checkLA = self.redParams.get("Leaf Base Avg") + self.redParams.get("Leaf Water Ratio Avg")*self.getVar("Amount of Water/week (mL)") + self.redParams.get("Leaf Outdoor Ratio Avg")*self.getVar("Outdoor?")
            checkLSD = self.redParams.get("Leaf Base Stdev") + self.redParams.get("Leaf Water Ratio Stdev")*self.getVar("Amount of Water/week (mL)") + self.redParams.get("Leaf Outdoor Ratio Stdev")*self.getVar("Outdoor?")
            checkFA = self.redParams.get("Flower Base Avg") + self.redParams.get("Flower Water Ratio Avg")*self.getVar("Amount of Water/week (mL)") + self.redParams.get("Flower Outdoor Ratio Avg")*self.getVar("Outdoor?")
            checkFSD = self.redParams.get("Flower Base Stdev")  + self.redParams.get("Flower Outdoor Ratio Stdev")*self.getVar("Outdoor?")
        else:
            checkLA = self.purpleParams.get("Leaf Base Avg") + self.purpleParams.get("Leaf Water Ratio Avg")*self.getVar("Amount of Water/week (mL)") + self.purpleParams.get("Leaf Outdoor Ratio Avg")*self.getVar("Outdoor?")
            checkLSD = self.purpleParams.get("Leaf Base Stdev") + self.purpleParams.get("Leaf Water Ratio Stdev")*self.getVar("Amount of Water/week (mL)") + self.purpleParams.get("Leaf Outdoor Ratio Stdev")*self.getVar("Outdoor?")
            checkFA = self.purpleParams.get("Flower Base Avg") + self.purpleParams.get("Flower Water Ratio Avg")*self.getVar("Amount of Water/week (mL)") + self.purpleParams.get("Flower Outdoor Ratio Avg")*self.getVar("Outdoor?")
            checkFSD = self.purpleParams.get("Flower Base Stdev") + self.purpleParams.get("Flower Outdoor Ratio Stdev")*self.getVar("Outdoor?")
        checkLeafSA = checkLA + checkLSD*self.lavg
        for v in self.model.getVars():
            print('Gurobi Result: %s: %g' % (v.varName, v.x))
            if v.varName == "Total Leaf Surface Area Average":
                print('\tCheck Result: ' + str(checkLA))
            elif v.varName == 'Total Leaf Surface Area Standard Deviation':
                print('\tCheck Result: ' + str(checkLSD))
            elif v.varName == 'Flower Petal Height Average':
                print('\tCheck Result: ' + str(checkFA))
            elif v.varName == 'Flower Petal Height Standard Deviation':
                print('\tCheck Result: ' + str(checkFSD))

        print('\nGurobi Stem + Flower Height (obj): %g' % self.getObj())
        print('\tCheck Stem Height: ' + str(0.1*checkLeafSA + 0.05*checkLeafSA*self.savg))
        print('\tCheck Flower Height: ' + str(checkFA + checkFSD*self.favg))
        print('\tCheck Total Height (obj): ' + str(0.1*checkLeafSA + 0.05*checkLeafSA*self.savg + checkFA + checkFSD*self.favg))