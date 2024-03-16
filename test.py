# import math
# import numpy as np
# import matplotlib.pyplot as plt
from package.PointG import PointG as Point
from package.GridG import GridG as Grid
import json
from package.statistics import graph_avg, graph_cmpr, to_json_file, run_and_save, graph
from package.GridPointsStruct import GridPoints

# run_and_save("Data", Grid.random_greedy, ns=range(3, 4), ds=range(2, 10))

graph("Data/random_greedy.JSON", runner="d", base=(3, 2, 2))

# g = Grid(2, 3)
# VP = GridPoints.fromGrid([], g)

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