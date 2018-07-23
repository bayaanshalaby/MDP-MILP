from gurobipy import *
import numpy as np

class StemFlowerRootsModel:
    def __init__(self, name, randomSeed, n):
        self.name = name 
        self.randomSeed = randomSeed
        self.n = int(n)
        self.model = Model(self.name)
        self.redParams = {"Leaf Base Avg" : 131,
                          "Leaf Water Ratio Avg" : 0.05,
                          "Leaf Outdoor Ratio Avg" : 20,
                          "Leaf Pellets Ratio Avg": -15,
                          "Leaf Base Stdev" : 65,
                          "Leaf Water Ratio Stdev": -0.001,
                          "Leaf Outdoor Ratio Stdev": 1,
                          "Flower Base Avg": 6,
                          "Flower Water Ratio Avg": -0.001,
                          "Flower Outdoor Ratio Avg": 2,
                          "Flower Base Stdev": 1.35,
                          "Flower Outdoor Ratio Stdev": 1,
                          "Roots Base Avg": 15,
                          "Roots Pellets Ratio Avg": 1.65,
                          "Roots Outdoor Ratio Avg": 0.25,
                          "Roots Base Stdev": 1,
                          "Roots Outdoor Ratio Stdev": 1}
        self.purpleParams = {"Leaf Base Avg" : 150,
                          "Leaf Water Ratio Avg" : 0.005,
                          "Leaf Outdoor Ratio Avg" : 5,
                          "Leaf Pellets Ratio Avg": -5,
                          "Leaf Base Stdev" : 30,
                          "Leaf Water Ratio Stdev": -0.005,
                          "Leaf Outdoor Ratio Stdev": 1,
                          "Flower Base Avg": 8,
                          "Flower Water Ratio Avg": -0.0015,
                          "Flower Outdoor Ratio Avg": 1,
                          "Flower Base Stdev": 0.75,
                          "Flower Outdoor Ratio Stdev": 1,
                          "Roots Base Avg": 16,
                          "Roots Pellets Ratio Avg": 0.45,
                          "Roots Outdoor Ratio Avg": 0.25,
                          "Roots Base Stdev": 2,
                          "Roots Outdoor Ratio Stdev": 1}
        self.costParams = {"Red Tulip" : 1.5, 
                           "Purple Tulip": 1.0, 
                           "Water": 0.015,
                           "Outdoor": 2,
                           "Pellets": 0.05}
        self.buildModel()
        
    def buildModel(self):
        self.model.setParam('OutputFlag', 0)

        # Create Variables 
        tulip_type = self.model.addVar(vtype = GRB.BINARY, name = "Tulip Type")
        water = self.model.addVar(lb = 250, ub = 1000, name = "Amount of Water/week (mL)")
        outdoor = self.model.addVar(vtype = GRB.BINARY, name = "Outdoor?")
        pellets = self.model.addVar(lb = 2, ub = 5, vtype = GRB.INTEGER, name = "Number of Fertilizer Pellets")
        lsaavg = self.model.addVar(name = "Total Leaf Surface Area Average")
        lsastdev = self.model.addVar(name = "Total Leaf Surface Area Standard Deviation")
        flavg = self.model.addVar(name = "Flower Petal Height Average")
        flstdev = self.model.addVar(name = "Flower Petal Height Standard Deviation")
        roavg = self.model.addVar(name = "Roots Length Average")
        rostdev = self.model.addVar(name = "Roots Length Standard Deviation")
        
        # Set objective 
        np.random.seed(self.randomSeed)
        lnorms = np.random.standard_normal(self.n)
        self.lavg = np.mean(lnorms)
        snorms = np.random.standard_normal(self.n)
        self.savg = np.mean(snorms)
        fnorms = np.random.standard_normal(self.n)
        self.favg = np.mean(fnorms)
        rnorms = np.random.standard_normal(self.n)
        self.ravg = np.mean(rnorms)
        
        leaf = (1/self.n)*(sum(lsaavg + lsastdev*lnorm for lnorm in lnorms))
        stem = (1/self.n)*(sum(0.1*leaf + 0.05*leaf*snorm for snorm in snorms))
        flower = (1/self.n)*(sum(flavg + flstdev*fnorm for fnorm in fnorms))
        roots = (1/self.n)*(sum(roavg + rostdev*rnorm for rnorm in rnorms))
        self.model.setObjective(stem + flower + roots, GRB.MAXIMIZE)
        

        # Set constraints 
        M = 10000
        
        #Leaf Constraints     
        # Average constraints
        self.model.addConstr(lsaavg <= self.redParams.get("Leaf Base Avg") 
                             + self.redParams.get("Leaf Water Ratio Avg")*water 
                             + self.redParams.get("Leaf Outdoor Ratio Avg")*outdoor
                             + self.redParams.get("Leaf Pellets Ratio Avg")*pellets + M*(1 - tulip_type))
        self.model.addConstr(lsaavg >= self.redParams.get("Leaf Base Avg") 
                             + self.redParams.get("Leaf Water Ratio Avg")*water 
                             + self.redParams.get("Leaf Outdoor Ratio Avg")*outdoor 
                             + self.redParams.get("Leaf Pellets Ratio Avg")*pellets- M*(1 - tulip_type))
        self.model.addConstr(lsaavg <= self.purpleParams.get("Leaf Base Avg") 
                             + self.purpleParams.get("Leaf Water Ratio Avg")*water 
                             + self.purpleParams.get("Leaf Outdoor Ratio Avg")*outdoor 
                             + self.purpleParams.get("Leaf Pellets Ratio Avg")*pellets + M*tulip_type)
        self.model.addConstr(lsaavg >= self.purpleParams.get("Leaf Base Avg") 
                             + self.purpleParams.get("Leaf Water Ratio Avg")*water 
                             + self.purpleParams.get("Leaf Outdoor Ratio Avg")*outdoor 
                             + self.purpleParams.get("Leaf Pellets Ratio Avg")*pellets - M*tulip_type)
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
      
        
        # Roots Constraints
        #Average 
        self.model.addConstr(roavg <= self.redParams.get("Roots Base Avg") 
                             + self.redParams.get("Roots Pellets Ratio Avg")*pellets
                             + self.redParams.get("Roots Outdoor Ratio Avg")*outdoor + M*(1 - tulip_type))
        self.model.addConstr(roavg >= self.redParams.get("Roots Base Avg") 
                             + self.redParams.get("Roots Pellets Ratio Avg")*pellets
                             + self.redParams.get("Roots Outdoor Ratio Avg")*outdoor - M*(1 - tulip_type))
        self.model.addConstr(roavg <= self.purpleParams.get("Roots Base Avg") 
                             + self.purpleParams.get("Roots Pellets Ratio Avg")*pellets
                             + self.purpleParams.get("Roots Outdoor Ratio Avg")*outdoor + M*tulip_type)
        self.model.addConstr(roavg >= self.purpleParams.get("Roots Base Avg") 
                             + self.purpleParams.get("Roots Pellets Ratio Avg")*pellets
                             + self.purpleParams.get("Roots Outdoor Ratio Avg")*outdoor - M*tulip_type)

        # Standard Deviation 
        self.model.addConstr(rostdev <= self.redParams.get("Roots Base Stdev") 
                             + self.redParams.get("Roots Outdoor Ratio Stdev")*outdoor + M*(1 - tulip_type))
        self.model.addConstr(rostdev >= self.redParams.get("Roots Base Stdev") 
                             + self.redParams.get("Roots Outdoor Ratio Stdev")*outdoor - M*(1 - tulip_type))
        self.model.addConstr(rostdev <= self.purpleParams.get("Roots Base Stdev") 
                             + self.purpleParams.get("Roots Outdoor Ratio Stdev")*outdoor + M*tulip_type)
        self.model.addConstr(rostdev >= self.purpleParams.get("Roots Base Stdev") 
                             + self.purpleParams.get("Roots Outdoor Ratio Stdev")*outdoor - M*tulip_type)
        
        # Water vs. pellets constraint
        self.model.addConstr(water >= 200*pellets)

        # Budget Constraint
        self.model.addConstr(self.costParams.get("Red Tulip")*tulip_type
                             + self.costParams.get("Purple Tulip")*(1 - tulip_type) 
                             + self.costParams.get("Water")*water 
                             + self.costParams.get("Outdoor")*(1 - outdoor) 
                             + self.costParams.get("Pellets")*pellets <= 12)

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
            stemHeight = np.random.normal(0.1*leafSA, 0.01*leafSA)
            flHeight = np.random.normal(self.getVar("Flower Petal Height Average"), self.getVar("Flower Petal Height Standard Deviation"))
            roLength = np.random.normal(self.getVar("Roots Length Average"), self.getVar("Roots Length Standard Deviation"))
            avgReward += stemHeight + flHeight + roLength
            i += 1
        return avgReward/trials
    
    def testResults(self):
        if self.getVar("Tulip Type") == 1:
            checkLA = self.redParams.get("Leaf Base Avg") + self.redParams.get("Leaf Water Ratio Avg")*self.getVar("Amount of Water/week (mL)") + self.redParams.get("Leaf Outdoor Ratio Avg")*self.getVar("Outdoor?") + self.redParams.get("Leaf Pellets Ratio Avg")*self.getVar("Number of Fertilizer Pellets")
            checkLSD = self.redParams.get("Leaf Base Stdev") + self.redParams.get("Leaf Water Ratio Stdev")*self.getVar("Amount of Water/week (mL)") + self.redParams.get("Leaf Outdoor Ratio Stdev")*self.getVar("Outdoor?")
            checkFA = self.redParams.get("Flower Base Avg") + self.redParams.get("Flower Water Ratio Avg")*self.getVar("Amount of Water/week (mL)") + self.redParams.get("Flower Outdoor Ratio Avg")*self.getVar("Outdoor?")
            checkFSD = self.redParams.get("Flower Base Stdev")  + self.redParams.get("Flower Outdoor Ratio Stdev")*self.getVar("Outdoor?")
            checkRA = self.redParams.get("Roots Base Avg") + self.redParams.get("Roots Pellets Ratio Avg")*self.getVar("Number of Fertilizer Pellets") + self.redParams.get("Roots Outdoor Ratio Avg")*self.getVar("Outdoor?")
            checkRSD = self.redParams.get("Roots Base Stdev") + self.redParams.get("Roots Outdoor Ratio Stdev")*self.getVar("Outdoor?")
        else:
            checkLA = self.purpleParams.get("Leaf Base Avg") + self.purpleParams.get("Leaf Water Ratio Avg")*self.getVar("Amount of Water/week (mL)") + self.purpleParams.get("Leaf Outdoor Ratio Avg")*self.getVar("Outdoor?") + self.purpleParams.get("Leaf Pellets Ratio Avg")*self.getVar("Number of Fertilizer Pellets")
            checkLSD = self.purpleParams.get("Leaf Base Stdev") + self.purpleParams.get("Leaf Water Ratio Stdev")*self.getVar("Amount of Water/week (mL)") + self.purpleParams.get("Leaf Outdoor Ratio Stdev")*self.getVar("Outdoor?")
            checkFA = self.purpleParams.get("Flower Base Avg") + self.purpleParams.get("Flower Water Ratio Avg")*self.getVar("Amount of Water/week (mL)") + self.purpleParams.get("Flower Outdoor Ratio Avg")*self.getVar("Outdoor?")
            checkFSD = self.purpleParams.get("Flower Base Stdev") + self.purpleParams.get("Flower Outdoor Ratio Stdev")*self.getVar("Outdoor?")
            checkRA = self.purpleParams.get("Roots Base Avg") + self.purpleParams.get("Roots Pellets Ratio Avg")*self.getVar("Number of Fertilizer Pellets") + self.purpleParams.get("Roots Outdoor Ratio Avg")*self.getVar("Outdoor?")
            checkRSD = self.purpleParams.get("Roots Base Stdev") + self.purpleParams.get("Roots Outdoor Ratio Stdev")*self.getVar("Outdoor?")
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
            elif v.varName == 'Roots Length Average':
                print('\tCheck Result: ' + str(checkRA))
            elif v.varName == 'Roots Length Standard Deviation':
                print('\tCheck Result: ' + str(checkRSD))

        print('\nGurobi Stem + Flower Height (obj): %g' % self.getObj())
        print('\tCheck Stem Height: ' + str(0.1*checkLeafSA + 0.05*checkLeafSA*self.savg))
        print('\tCheck Flower Height: ' + str(checkFA + checkFSD*self.favg))
        print('\tCheck Roots Length: ' + str(checkRA + checkRSD*self.ravg))
        print('\tCheck Total Height (obj): ' + str(0.1*checkLeafSA + 0.05*checkLeafSA*self.savg + checkFA + checkFSD*self.favg + checkRA + checkRSD*self.ravg)) 
