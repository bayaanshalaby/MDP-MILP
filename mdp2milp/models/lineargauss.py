class LinearGaussianModel:

    def __init__(self, name):
        self.name = name
        self.inputs = {}
        self.outputs = {}
        self.params = {}

    def addInputVariable(self, id, description, lb=None, ub=None):
        pass

    def addOutputVariable(self, id, description):
        pass

    def setLinearLocationParameter(self, id, vars, weights, b):
        pass

    def setLinearScaleParameter(self, id, vars, weights, b):
        pass

    def sample(self, id, size):
        pass
