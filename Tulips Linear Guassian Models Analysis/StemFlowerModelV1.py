from gurobipy import *
import numpy as np
import time 

class StemFlowerModel:
    def __init__(self, name, randomSeed, n):
        self.name = name
        self.randomSeed = randomSeed
        self.n = int(n)
        self.model = Model(self.name)
        self.buildModel()
    
    def buildModel(self):
        start_time = time.time()
        self.model.setParam('OutputFlag', 0)

        # Create Variables 
        tulip_type = self.model.addVar(vtype = GRB.BINARY, name = "Tulip Type")
        water = self.model.addVar(lb = 250, ub = 1000, name = "Amount of Water/week (mL)")
        outdoor = self.model.addVar(vtype = GRB.BINARY, name = "Outdoor?")
        lsa = self.model.addVar(name = "Total Leaf Surface Area")
        lsaavg = self.model.addVar(name = "Total Leaf Surface Area Average")
        lsastdev = self.model.addVar(name = "Total Leaf Surface Area Standard Deviation")
        flavg = self.model.addVar(name = "Flower Petal Height Average")
        flstdev = self.model.addVar(name = "Flower Petal Height Standard Deviation")
        self.model.update()
        
        # Set objective 
        # Monte Carlo-ing Expectation
        i = 0
        leaf = LinExpr()
        stem = LinExpr()
        flower = LinExpr()
        while i < self.n:

            leaf += lsaavg + lsastdev*np.random.standard_normal()
            stem += 0.1*(lsa) + 0.05*(lsa)*np.random.standard_normal()
            flower += flavg + flstdev*np.random.standard_normal()

            i += 1

        # Set objective
        self.model.setObjective((1/self.n)*(stem + flower), GRB.MAXIMIZE)
        
        # Set constraints 
        M = 10000
        
        #Leaf Constraints     
        # Average constraints
        self.model.addConstr(lsaavg <= 131 + 0.05*water + 20*outdoor + M*(1 - tulip_type))
        self.model.addConstr(lsaavg >= 131 + 0.05*water + 20*outdoor - M*(1 - tulip_type))
        self.model.addConstr(lsaavg <= 150 + 0.005*water + 5*outdoor + M*tulip_type)
        self.model.addConstr(lsaavg >= 150 + 0.005*water + 5*outdoor - M*tulip_type)
        # Standard Deviation Constraints 
        self.model.addConstr(lsastdev <=  65 - 0.001*water + outdoor + M*(1 - tulip_type))
        self.model.addConstr(lsastdev >=  65 - 0.001*water + outdoor - M*(1 - tulip_type))
        self.model.addConstr(lsastdev <=  30 - 0.005*water + outdoor + M*tulip_type)
        self.model.addConstr(lsastdev >= 30 - 0.005*water + outdoor - M*tulip_type)
        # lsa constraints
        self.model.addConstr(lsa <= (1/self.n)*leaf)
        self.model.addConstr(lsa >= (1/self.n)*leaf)
        
        # Flower Constraints 
        # Average Constraints 
        self.model.addConstr(flavg <= 6 - 0.001*water + 2.0*(1 - outdoor) + M*(1 - tulip_type))
        self.model.addConstr(flavg >= 6 - 0.001*water + 2.0*(1 - outdoor) - M*(1 - tulip_type))
        self.model.addConstr(flavg <= 8 - 0.0015*water + 1.0*(1 - outdoor) + M*tulip_type)
        self.model.addConstr(flavg >= 8 - 0.0015*water + 1.0*(1 - outdoor) - M*tulip_type)
        # If tulip_type = 1, flstdev = 1.35 + outdoor, else flstdev = 0.75 + outdoor
        self.model.addConstr(flstdev <= 1.35 + outdoor + M*(1 - tulip_type))
        self.model.addConstr(flstdev >= 1.35 + outdoor - M*(1 - tulip_type))
        self.model.addConstr(flstdev <= 0.75 + outdoor + M*tulip_type)
        self.model.addConstr(flstdev >= 0.75 + outdoor - M*tulip_type)

        #Budget Constraint
        self.model.addConstr(1.5*tulip_type + 1.0*(1 - tulip_type) + 0.015*water + 2*(1 - outdoor) <= 12)
        
        # Optimize model
        self.model.optimize()
        end_time = time.time()
        self.runTime = end_time - start_time 
        
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
    
    def getRunTime(self):
        return self.runTime
    
    def getOptimizationTime(self):
        return self.model.Runtime
    
    def getSimplexIters(self):
        return self.model.IterCount