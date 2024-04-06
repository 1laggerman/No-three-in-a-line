# import math
import numpy as np
# import matplotlib.pyplot as plt
from package.Point import Point as Point
from package.Grid import Grid as Grid
import json
from package.statistics import graph_avg, graph_cmpr, to_json_file, run_and_save, graph
from package.GridPointsStruct import GridPoints, collision

import itertools as it
from copy import deepcopy


n = 4
d = 2
k = 2
gp = GridPoints(n=n, d=d, k_in_line=k)
gp.add(Point(0, 0, n=n))
gp.add(Point(1, 1, n=n))
gp.add(Point(2, 2, n=n))
gp.add(Point(3, 3, n=n))

print(gp)

print(gp.collision_mat[0, 0].lines)
print(gp.collision_mat[1, 1].lines)
print(gp.collision_mat[2, 2].lines)
print(gp.collision_mat[3, 3].lines)

gp.remove(Point(0, 0, n=n))

print(gp)

print(gp.collision_mat[0, 0].lines)
print(gp.collision_mat[1, 1].lines)
print(gp.collision_mat[2, 2].lines)
print(gp.collision_mat[3, 3].lines)
