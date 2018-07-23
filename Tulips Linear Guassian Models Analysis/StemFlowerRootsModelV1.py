from gurobipy import *
import numpy as np

class StemFlowerRootsModel:
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
        outdoor = self.model.addVar(vtype = GRB.BINARY, name = "Outdoor?")
        pellets = self.model.addVar(lb = 2, ub = 5, vtype = GRB.INTEGER, name = "Number of Fertilizer Pellets")
        lsa = self.model.addVar(name = "Total Leaf Surface Area")
        lsaavg = self.model.addVar(name = "Total Leaf Surface Area Average")
        lsastdev = self.model.addVar(name = "Total Leaf Surface Area Standard Deviation")
        flavg = self.model.addVar(name = "Flower Petal Height Average")
        flstdev = self.model.addVar(name = "Flower Petal Height Standard Deviation")
        roavg = self.model.addVar(name = "Roots Length Average")
        rostdev = self.model.addVar(name = "Roots Length Standard Deviation")
        
        # Set objective 
        i = 0
        leaf = LinExpr()
        stem = LinExpr()
        flower = LinExpr()
        roots = LinExpr()
        while i < self.n:

            leaf += lsaavg + lsastdev*np.random.standard_normal()
            stem += 0.1*(lsa) + 0.05*(lsa)*np.random.standard_normal()
            flower += flavg + flstdev*np.random.standard_normal() 
            roots += roavg + rostdev*np.random.standard_normal() 

            i += 1
        self.model.setObjective((1/self.n)*(stem + flower + roots), GRB.MAXIMIZE)
        

        # Set constraints 
        M = 10000
        
        #Leaf Constraints     
        # Average constraints
        self.model.addConstr(lsaavg <= 131 + 0.05*water + 20*outdoor - 15*pellets + M*(1 - tulip_type))
        self.model.addConstr(lsaavg >= 131 + 0.05*water + 20*outdoor - 15*pellets - M*(1 - tulip_type))
        self.model.addConstr(lsaavg <= 150 + 0.005*water + 5*outdoor - 5*pellets + M*tulip_type)
        self.model.addConstr(lsaavg >= 150 + 0.005*water + 5*outdoor - 5*pellets - M*tulip_type)
        # Standard Deviation Constraints 
        self.model.addConstr(lsastdev <=  65 - 0.001*water + outdoor + M*(1 - tulip_type))
        self.model.addConstr(lsastdev >=  65 - 0.001*water + outdoor - M*(1 - tulip_type))
        self.model.addConstr(lsastdev <=  30 - 0.005*water + outdoor + M*tulip_type)
        self.model.addConstr(lsastdev >= 30 - 0.005*water + outdoor - M*tulip_type)
        self.model.addConstr(lsa <= (1/self.n)*leaf)
        self.model.addConstr(lsa >= (1/self.n)*leaf)
        
        # Flower Constraints 
        # Average Constraints 
        self.model.addConstr(flavg <= 6 - 0.001*water + 2.0*(1 - outdoor) + M*(1 - tulip_type))
        self.model.addConstr(flavg >= 6 - 0.001*water + 2.0*(1 - outdoor) - M*(1 - tulip_type))
        self.model.addConstr(flavg <= 8 - 0.0015*water + 1.0*(1 - outdoor) + M*tulip_type)
        self.model.addConstr(flavg >= 8 - 0.0015*water + 1.0*(1 - outdoor) - M*tulip_type)
        # Standard Deviation Constraints 
        self.model.addConstr(flstdev <= 1.35 + outdoor + M*(1 - tulip_type))
        self.model.addConstr(flstdev >= 1.35 + outdoor - M*(1 - tulip_type))
        self.model.addConstr(flstdev <= 0.75 + outdoor + M*tulip_type)
        self.model.addConstr(flstdev >= 0.75 + outdoor - M*tulip_type)

        # Roots Constraints
        #Average 
        self.model.addConstr(roavg <= 15 + 1.65*pellets + 0.25*outdoor + M*(1 - tulip_type))
        self.model.addConstr(roavg >= 15 + 1.65*pellets + 0.25*outdoor - M*(1 - tulip_type))
        self.model.addConstr(roavg <= 16 + 0.45*pellets + 0.25*outdoor + M*tulip_type)
        self.model.addConstr(roavg >= 16 + 0.45*pellets + 0.25*outdoor - M*tulip_type)
        # Standard Deviation 
        self.model.addConstr(rostdev <= 1 + outdoor + M*(1 - tulip_type))
        self.model.addConstr(rostdev >= 1 + outdoor - M*(1 - tulip_type))
        self.model.addConstr(rostdev <= 2 + outdoor + M*tulip_type)
        self.model.addConstr(rostdev >= 2 + outdoor - M*tulip_type)
        
        # Water vs. pellets constraint
        self.model.addConstr(water >= 200*pellets)

        # Budget Constraint
        self.model.addConstr(1.5*tulip_type + 1.0*(1 - tulip_type) + 0.015*water + 2*(1 - outdoor) + 0.05*pellets <= 12)

        # Optimize model
        self.model.optimize()
        
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
            stemHeight = np.random.normal(0.1*leafSA, 0.01*leafSA)
            flHeight = np.random.normal(self.getVar("Flower Petal Height Average"), self.getVar("Flower Petal Height Standard Deviation"))
            roLength = np.random.normal(self.getVar("Roots Length Average"), self.getVar("Roots Length Standard Deviation"))
            avgReward += stemHeight + flHeight + roLength
            i += 1
        return avgReward/trials