# import math
import numpy as np
# import matplotlib.pyplot as plt
from package.Point import Point as Point
from package.Grid import Grid as Grid
import json
from package.statistics import graph_avg, graph_cmpr, to_json_file, run_and_save, graph
from package.GridPointsStruct import GridPoints
from package.collision import collision

import itertools as it
from copy import deepcopy

# a = np.full((4,) * 2, fill_value=None, dtype=collision)

# for cords in it.product(range(4), repeat=2):
#     c = cords[::-1]
#     a[c] = collision()
    
# print(np.min(a))


n = 4
d = 2
k = 2



# g = Grid(n=n, d=d)
# g.min_conflict(100, False, allowed_in_line=k)


gp: GridPoints = GridPoints(n=4, d=2, k_in_line=2)

gp.add(Point(1, 0, n=n))
gp.add(Point(0, 1, n=n))
gp.add(Point(2, 1, n=n))

gp.add_collision(Point(1, 1, n=n), [])

print(gp)

legal_collision = np.logical_and(gp.collision_mat > 0, gp.idx_mat <= 0)
l = np.where(legal_collision, gp.collision_mat, np.inf)
print(l)
# print(type(l[0, 0]))
print(np.argmin(l))
argmin_index = np.unravel_index(np.argmin(np.where(legal_collision, gp.collision_mat, np.inf)), gp.idx_mat.shape)
print(argmin_index)


# legal_collision = np.array([[False, False], [True, True]])
# mat = np.array([[2, 1], [2, 3]])
# a = np.where(legal_collision, mat, np.inf)
# argmin_index = np.unravel_index(np.argmin(a), a.shape)
# print(argmin_index)


# a = np.array([[True, False], [False, True]])
# b = np.array([[2, 1], [3, 3]])

# # Create a boolean mask where 'a' is False
# mask = a

# # Apply the mask to 'b' to filter out elements where 'a' is False
# filtered_b = np.where(mask, b, np.inf)

# # Find the indices of the minimum value in the filtered array
# argmin_index = np.unravel_index(np.argmin(filtered_b), filtered_b.shape)

# print("Indices of minimum value where 'a' is False:", argmin_index)