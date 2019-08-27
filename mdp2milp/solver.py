from models import lineargauss
from compiler import MILPCompiler
from optimizer import MILPOptimizer


import argparse
import numpy as np
import matplotlib.pyplot as plt


def parse_args():
    pass


def read_model(rddl):
    pass


def optimize(model, sample_sizes):
    # compile to MILP
    milp = MILPCompiler(model)

    # optimize MILP program
    opt = MILPOptimizer(milp)
    opt.optimize(args["sample_sizes"])

    return optimizer


def report(optimizer):
    rewards = opt.getObjective()
    actions = opt.getVariables()
    pass


if __name__ == '__main__':
    args = parse_args()

    # read Linear/PWL Gaussian model
    model = read_model(args["rddl"])

    # optimize the model
    optimizer = optimize(model, args["sample_sizes"])

    # results
    report(optimizer)
