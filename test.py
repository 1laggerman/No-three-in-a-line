import math
import numpy as np
import matplotlib.pyplot as plt
from package.PointG import PointG as Point
from package.GridG import GridG as Grid
from package.statistics import graph_avg, graph_cmpr


from package.validPointsStruct import validPoints

n = 3
d = 4

g = Grid(n=n, d=d)
# print("max: ", int(2 * math.pow(n, d - 1)), "points")
# print(g.random_greedy())
graph_cmpr(Grid.random_greedy, iters = 10, rg=range(3, 7), base=3)