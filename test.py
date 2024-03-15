# import math
# import numpy as np
# import matplotlib.pyplot as plt
from package.PointG import PointG as Point
from package.GridG import GridG as Grid
# from package.statistics import graph_avg, graph_cmpr


from package.GridPointsStruct import GridPoints

g = Grid(2, 3)
# VP = GridPoints.fromGrid([], g)

n = 100
d = 2

g = Grid(n=n, d=d)
s = g.random_greedy(allowed_in_line=10)
print(s[1])

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