# import math
# import numpy as np
# import matplotlib.pyplot as plt
# from package.PointG import PointG as Point
from package.GridG import GridG as Grid
# from package.statistics import graph_avg, graph_cmpr


from package.GridPointsStruct import GridPoints

g = Grid(2, 3)
VP = GridPoints.fromGrid([], g)

# n = 3
# d = 4

# g = Grid(n=n, d=d)
# print("max: ", int(2 * math.pow(n, d - 1)), "points")
# print(g.random_greedy())
# graph_avg(Grid.random_greedy, iters = 10, ns=range(3, 5), ds=range(3, 4))

# g = Grid(3, 2)
# VP = GridPoints(g.getAllValidPoints(), 3, 2)

# VP.remove(Point(0, 0))
# VP.remove(Point(2, 2))
# VP.remove(Point(1, 1))

# valid_points = GridPoints([Point(1, 2), Point(1, 0), Point(2, 0), Point(0, 1), Point(0, 2), Point(2, 1)], 3, 2)

# print(valid_points == VP)