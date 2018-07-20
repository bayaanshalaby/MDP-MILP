from gurobipy import Model


class MILPCompiler:

    def __init__(self, name, model):
        self.name = name
        self.model = model

    def build_milp(self, model, **options):
        self.milp = Model(self.name)

        for param, value in options.items():
            self.milp.setParam(param, value)

        # ...
        return self.milp

    def _compile_variables(self):
        pass

    def _compile_constraints(self, bigM=1000):
        pass

    def _compile_objective(self, vars, N):
        pass
