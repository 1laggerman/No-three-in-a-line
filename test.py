# import math
import numpy as np
# import matplotlib.pyplot as plt
from package.Point import Point as Point
from package.Grid import Grid as Grid
import json
from package.statistics import to_json_file, run_and_save, graph, run, RunData
from package.GridPointsStruct import GridPoints
from package.collision import collision
import random

import itertools as it
from copy import deepcopy
import tqdm
import time

# a = np.full((4,) * 2, fill_value=None, dtype=collision)

# for cords in it.product(range(4), repeat=2):
#     c = cords[::-1]
#     a[c] = collision()
    
# print(np.min(a))
# i = 0
# with tqdm.tqdm(total=10) as bar:
#     while i < 10:
#         i += 1
#         bar.update(1)
#         time.sleep(1)
#         if i == 5:
#             bar.update(-i)
#             i = 0
#         time.sleep(0.5)


# n = 3
# d = 2
# k = 2

# print(run(func=Grid.min_conflict, ns=range(3, 5), ds=range(2, 4), ks=[2]))
# run_and_save(file_path="Data", func=Grid.min_conflict, ns=[n], ds=[d], ks=range(k, k+3), iters=1)
# run_and_save(file_path="Data", func=Grid.min_conflict, ns=[3], ds=range(2, 10), ks=[2], iters=10)
# graph('Data/min_conflict.JSON', runner='n', base=(n, d, k), stop_at=10)
# graph('Data/min_conflict.JSON', runner='k', base=(50, 2, 2), stop_at=20)

# g = Grid(n=n, d=d)
# rg = g.random_greedy(sorted=True, allowed_in_line=k)
# print(len(rg.chosen))
# g.add_points(rg.chosen)
# best = g.min_conflict(100, False, allowed_in_line=k, start_from=rg)

# g.add_points(best.chosen)
# g.draw_grid()

# gp = GridPoints(n=n, d=d, k_in_line=k)
# gp.add(Point(0, 0, n=n))
# gp.add(Point(1, 1, n=n))
# gp.add(Point(2, 2, n=n))

# suspects = np.where(gp.collision_mat > 0)
# print(suspects)
# for j in range(len(suspects[0])):
#     suspect_point = Point(*tuple([suspects[k][j] for k in range(d)]), n=n)


# print(np.apply_over_axes(collision.num, gp.collision_mat, axes=[0,1]))
# vectorized_func = np.vectorize(collision.num)
# collision_count = vectorized_func(gp.collision_mat)
# print(collision_count)
# collision_count = vectorized_func(gp.conflicted)



# a = np.array([[, np.inf], [1, 2]])
# print(np.min(a))

# conflicts = np.array([[True, False], [False, True]])
# collision_mat = np.array([[3, 1], [3, 2]])
# conflicts = np.where(conflicts, collision_mat, 0)
# conflicts = conflicts / np.sum(conflicts)
# print(conflicts)

# min_conflict_points = np.array([[True, False], [False, True]])
# indices = np.where(min_conflict_points)
# random_index = tuple(random.choice(indices) for indices in min_conflict_points)
# added_point = random.choice(indices)

# print(random_index)
# print(indices)

# print(added_point)
# gp: GridPoints = GridPoints(n=4, d=2, k_in_line=2)

# gp.add(Point(1, 1, n=n))
# print(gp)
# print(gp.collision_mat[1, 1].lines)
# print(gp.collision_mat[2, 2].lines)
# print(gp.collision_mat[1, 2].lines)
# print(gp.collision_mat[2, 1].lines)
# gp.add(Point(2, 2, n=n))
# print(gp)
# print(gp.collision_mat[1, 1].lines)
# print(gp.collision_mat[2, 2].lines)
# print(gp.collision_mat[1, 2].lines)
# print(gp.collision_mat[2, 1].lines)
# gp.add(Point(1, 2, n=n))
# print(gp)
# print(gp.collision_mat[1, 1].lines)
# print(gp.collision_mat[2, 2].lines)
# print(gp.collision_mat[1, 2].lines)
# print(gp.collision_mat[2, 1].lines)
# gp.add(Point(2, 1, n=n))
# print(gp)
# print(gp.collision_mat[1, 1].lines)
# print(gp.collision_mat[2, 2].lines)
# print(gp.collision_mat[1, 2].lines)
# print(gp.collision_mat[2, 1].lines)

# gp.add_collision(Point(1, 1, n=n), [])

# print(gp)

# legal_collision = np.logical_and(gp.collision_mat > 0, gp.idx_mat <= 0)
# l = np.where(legal_collision, gp.collision_mat, np.inf)
# print(l)
# # print(type(l[0, 0]))
# print(np.argmin(l))
# argmin_index = np.unravel_index(np.argmin(np.where(legal_collision, gp.collision_mat, np.inf)), gp.idx_mat.shape)
# print(argmin_index)


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