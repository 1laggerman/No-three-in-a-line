# import math
import numpy as np
# import matplotlib.pyplot as plt
from package.Point import Point as Point
from package.Grid import Grid as Grid
import json
from package.statistics import graph_avg, graph_cmpr, to_json_file, run_and_save, graph
from package.GridPointsStruct import GridPoints, collision

from copy import deepcopy



# run_and_save("Data", Grid.random_greedy, ns=range(3, 4), ds=range(2, 10))

# graph("Data/random_greedy.JSON", runner="d", base=(3, 2, 2))
n = 2
d = 3
# g = Grid(n, d)
# VP = GridPoints.fromGrid(g)

n = 2
d = 3

# def create_array_of_lists(n, d):
#     if d == 1:
#         return np.array([[] for _ in range(n)], dtype=object)
#     else:
#         return np.array([create_array_of_lists(n, d-1) for _ in range(n)], dtype=object)

# a = create_array_of_lists(n, d)

# a[0, 0, 0].append(3)
# print(a[0, 0, 0, 0])

# c_mat = np.full((3,) * 2, fill_value=collision(), dtype=collision)

# print(c_mat)
# p = Point(0, 0, n=3)
# p1 = Point(0, 0, n=3)
# a = [p]
# b = [p1]

# print(a == b)



# a: np.ndarray[collision]
# a = np.array([[collision(), collision()], [collision(), collision()]], dtype=collision)
# d: collision = a[0, 0]
# d.amount += 1
# print(a)

# a = np.full((2, 2), fill_value=collision(), dtype=collision)
# a[0, 0].amount = 1
# print(a)


gp = GridPoints(n=4, d=2, k_in_line=3)

gp.add(Point(0, 0, n=4))
gp.add(Point(1, 1, n=4))
gp.add(Point(2, 2, n=4))
# gp.add(Point(3, 3, n=4))

print(gp)

print(gp.get_lines(Point(3, 3, n=4), 3))

# gp = GridPoints(n=5, d=2, k_in_line=3)

# gp.add(Point(0, 0, n=5))
# gp.add(Point(1, 1, n=5))
# gp.add(Point(2, 2, n=5))
# gp.add(Point(3, 3, n=5))

# print(gp)

# gp = GridPoints(n = 3, d = 2, k_in_line=2)

# print(gp)

# gp.add(Point(0, 0, n=3))

# print(gp)

# gp.add(Point(0, 0, n=3))

# print(gp)

# a = []
# for i in range(n):
#     a.append([])
# for i in range(d - 1):
#     a = [deepcopy(a), deepcopy(a)]

# print(a)
# print(a[0])
# print(a[0][0])
# print(a[0][0][0])

# a[0][0][0].append(3)

# print(a)


# a = np.zeros((2,) * 3, dtype=list)
# a.fill(list())
# print('--------')
# for x in a.data:
#     print(x)
#     x = list()
# print('--------')
# print(a)
# a[0, 0, 0].append(3)
# a[0, 0, 0] = []
# print(a)

# n = 10
# d = 2
# k = 10

# g = Grid(n=n, d=d)
# s = g.random_greedy(allowed_in_line=k)
# print(s[1])

# new_data = [{
#     "n": n,
#     "d": d,
#     "k": k,
#     "avg_points": s[1],
#     "total_runs": 2
# }]

# to_json_file("Data", new_data, alg="random_greedy")

# # Define the filename for your JSON file
# filename = "Data/random_greedy.JSON"

# with open(filename, "r") as json_file:
#     existing_data = json.load(json_file)

# # Check if data for the given n, d, and k already exists
# print(existing_data)
# for new_item in new_data:
#     found = False
#     for item in existing_data:
#         print(item)
#         if item["n"] == new_item["n"] and item["d"] == new_item["d"] and item["k"] == new_item["k"]:
#             item["avg_points"] = (item["avg_points"] * item["total_runs"] + new_item["avg_points"] * new_item["total_runs"]) / (item["total_runs"] + new_item["total_runs"])
#             item["total_runs"] += new_item["total_runs"]
#             found = True
#             break
#     if not found:
#         existing_data.append(new_data)

# # If data doesn't exist, add it to the existing data


# # Write the updated data back to the file
# with open(filename, "w") as json_file:
#     json.dump(existing_data, json_file)

# print("Data has been updated in", filename)
# valid_points = GridPoints(g.getAllValidPoints(), n=n, d=d)
# chosen_points = GridPoints([], n=n, d=d)

# l: list[Point] = [Point(0, 0, n=3), Point(2, 0, n=3), Point(2, 1, n=3), Point(3, 0, n=3), Point(3, 3, n=3), Point(1, 2, n=3)]
# l.extend([Point(3, 1, n=3), Point(1, 3, n=3), Point(0, 2, n=3), Point(2, 3, n=3), Point(1, 1, n=3)])
# for point in l:
#     added_point = valid_points.l[valid_points.m[tuple(point.cords)]]
#     valid_points = g.removeInValidPoints([added_point], valid_points, chosen_points, k_in_line=3)
#     chosen_points.append(added_point)

# added_point = valid_points.l[valid_points.m[tuple(Point(3, 0, n=3).cords)]]
# valid_points = g.removeInValidPoints([added_point], valid_points, chosen_points, k_in_line=3)
# chosen_points.append(added_point)

# added_point = valid_points.l[valid_points.m[tuple(Point(3, 2, n=3).cords)]]
# valid_points = g.removeInValidPoints([added_point], valid_points, chosen_points, k_in_line=3)
# chosen_points.append(added_point)

# added_point = valid_points.l[valid_points.m[tuple(Point(2, 3, n=3).cords)]]
# valid_points = g.removeInValidPoints([added_point], valid_points, chosen_points, k_in_line=3)
# chosen_points.append(added_point)

# added_point = valid_points.l[valid_points.m[tuple(Point(3, 3, n=3).cords)]]
# valid_points = g.removeInValidPoints([added_point], valid_points, chosen_points, k_in_line=3)
# chosen_points.append(added_point)

# added_point = valid_points.l[valid_points.m[tuple(Point(1, 2, n=3).cords)]]
# valid_points = g.removeInValidPoints([added_point], valid_points, chosen_points, k_in_line=3)
# chosen_points.append(added_point)

# added_point = valid_points.l[valid_points.m[tuple(Point(1, 2, n=3).cords)]]
# valid_points = g.removeInValidPoints([added_point], valid_points, chosen_points, k_in_line=3)
# chosen_points.append(added_point)


# print(valid_points)
# print(chosen_points)
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