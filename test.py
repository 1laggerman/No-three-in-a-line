import matplotlib.pyplot as plt
import numpy as np
import itertools as it
import random as rand
import copy
# from numba import jit, cuda
from timeit import default_timer as timer

class Point:
    x = 0
    y = 0
    z = 0

    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"
    def __repr__(self):
        return str(self)
        
    def __add__(self, __other: "Point"):
        return Point(self.x + __other.x, self.y + __other.y, self.z + __other.z)
    
    def __eq__(self, __value: "Point") -> bool:
        if self.x == __value.x and self.y == __value.y and self.z == __value.z:
            return True
        return False
    
    def __gt__(self, __other: "Point") -> bool:
        if self.z != __other.z:
            return self.z > __other.z
        elif self.x != __other.x:
            return self.x > __other.x
        return self.y > __other.y
    
    def __ge__(self, __other: "Point") -> bool:
        if self.z != __other.z:
            return self.z > __other.z
        if self.x != __other.x:
            return self.x >= __other.x
        return self.y >= __other.y
    
    def __hash__(self) -> int:
        return self.x + (self.y * self.n) + (self.z * pow(self.n, 2))
    
    def onTheSameLine(self, point2: "Point", point3: "Point"):
        
        if self == point2 or self == point3 or point2 == point3:
            return True
        
        dx2 = self.x - point2.x
        dx3 = self.x - point3.x
        dy2 = self.y - point2.y
        dy3 = self.y - point3.y
        
        if dx2 == 0 and dx3 == 0:
            # dx1 = 0, dx2 = 0
            if dy2 == 0 and dy3 == 0:
                return True
            elif dy2 == 0 or dy3 == 0:
                return False
            Myz2 = (self.z - point2.z) / dy2
            Myz3 = (self.z - point3.z) / dy3
            if Myz2 != Myz3:
                return False
            return True
        elif dx2 == 0 or dx3 == 0:
            return False

        Mxy2 = dy2 / dx2
        Mxy3 = dy3 / dx3
        if Mxy2 != Mxy3:
            return False
        Mxz2 = (self.z - point2.z) / dx2
        Mxz3 = (self.z - point3.z) / dx3
        if Mxz2 != Mxz3:
            return False
        return True

class Grid:
    points = list()
    n = 1
    d = 2
    solutions: list[tuple[int, list[Point]]]
    
    def __init__(self, n: int = 3, d: int = 2):
        self.n = n
        self.d = d
        
    def add_point(self, p: Point):
        self.points.append(p)
        
    def add_points(self, points_arr: list):
        for point in points_arr:
            self.points.append(point)
            
    def is_solution(self, points: list[Point]):
        points.extend(self.points)
        
        for point1, point2, point3 in it.combinations(points, 3):
            if point1.onTheSameLine(point2, point3):
                return False
        return True
    
    def getAllValidPoints(self, d: int = 2, z_layer: int = 0, chosen: list = list()):
        chosen.extend(self.points)
        ValidPoints: list[Point] = list()
        
        for z in range(self.n):
            for x in range(self.n):
                for y in range(self.n):
                    if d == 2:
                        if len(self.points) > 0:
                            z = chosen[0].z
                        else:
                            z = z_layer
                            
                    thisPoint = Point(x, y, z)
                    
                    if len(chosen) == 0:
                        ValidPoints.append(thisPoint)
                    elif len(chosen) == 1:
                        if thisPoint != chosen[0]:
                            ValidPoints.append(thisPoint)
                    else:
                        pointValid = True
                        for point1, point2 in it.combinations(chosen, 2):
                            if thisPoint.onTheSameLine(point1, point2):
                                pointValid = False
                        if pointValid:
                            ValidPoints.append(thisPoint)
                        
            if d == 2:
                break
                                
        return ValidPoints
    
    def find_max_solutions_2D(self):
        max = 2 * self.n
        if self.d == 3:
            max = max * self.n            
        valid = self.getAllValidPoints(d = self.d)
        max_solutions = (list([self.points]), len(self.points))
        
        if len(self.points) == 0:
            max_solutions = self.choose_2_Xpoints_recursive_from_valid(max, valid, 0, 0)
        else:
            print("ERROR!")
            return (0, 0)
        
        if max_solutions[1] < max:
            print("could not find max solution")
            return max_solutions
        self.solutions = list(enumerate(max_solutions[0]))
        
        return (len(self.solutions), max_solutions[1])
    
    def choose_2_Xpoints_recursive_from_valid(self, max: int, validPoints: list, x: int, z: int = 0, chosen_points: list = list()):
        current_max = (list([list.copy(chosen_points)]), len(chosen_points) + len(self.points))
        if current_max[1] == max:
            return current_max
        elif len(validPoints) < 2:
            if len(validPoints) == 1:
                current_max[0][0].append(validPoints[0])
            return current_max
        
        for i in range(len(validPoints)):
            if validPoints[i].x != x or validPoints[i].z != z:
                break
            chosen_points.append(validPoints[i])
            
            j = i + 1
            while j < len(validPoints):
                if validPoints[j].x != x or validPoints[j].z != z:
                    break
                chosen_points.append(validPoints[j])
                # call recursively to choose other points and get the max result:
                new_valid = self.removeInValidPoints_2_new(validPoints[i], validPoints[j], validPoints.copy(), chosen=chosen_points)
                if x + 1 == self.n:
                    x = -1
                    z = z + 1
                t = self.choose_2_Xpoints_recursive_from_valid(max, new_valid, x + 1, z, chosen_points=chosen_points)
                if t[1] > current_max[1]: # bigger max found, replace the old max
                    current_max = t
                elif t[1] == current_max[1] or t[1] == max: # found another solution(at least one) with the same max
                    self.union_solutions(current_max[0], t[0], current_max[1])
                chosen_points.pop()
                j = j + 1
            chosen_points.pop()
        
        return current_max
    
    def removeInValidPoints_2_new(self, added1: Point, added2: Point, valid: list, chosen: list = list()):
        
        if added1.x == added2.x and added1.z == added2.z:
            for i in range(self.n):
                try:
                    valid.remove(Point(added1.x, i, added1.z))
                except:
                    pass
                    
         
        for point1 in chosen:
            if point1 != added1 and point1 != added2:
                i = 0
                while i < len(valid):
                    if added1.onTheSameLine(point1, valid[i]) or added2.onTheSameLine(point1, valid[i]):
                        valid.remove(valid[i])
                        i = i - 1
                    i = i + 1
        return valid
    
    def union_solutions(self, set1: list, set2: list, length: int):
        for solution1 in set1:
            for solution2 in set2:
                i = 0
                while i < length and solution1[i] == solution2[i]:
                    i = i + 1
                if i == length:
                    set2.remove(solution2)
            
        # add all valid solutions:
        set1.extend(set2)

    # @jit(forceobj=True)
    def order_2D_solutions(self, proba: float = 1, method = 'valid_points'):
        
        print('flag 6')
        
        max = (list(), 0)
        valid_points = self.getAllValidPoints(d=3)
        while(valid_points[0].z == 0):
            valid_points.pop(0)
        
        for solution in self.solutions:
            xy_mat = np.zeros((self.n, self.n))
            chosen = list()
            for point in solution[1]:
                chosen.append(point)
                xy_mat[point.x, point.y] = 1
                
            if method == 'valid_points':
                t = self.choose_solution_recursive(list([solution[0]]), [index for index, _ in self.solutions], chosen, valid_points, xy_mat, (False, True))
            elif method == 'valid_matrix':
                t = self.choose_solution_recursive(list([solution[0]]), [index for index, _ in self.solutions], chosen, valid_points, xy_mat, (True, False))
            elif method == 'All':
                t = self.choose_solution_recursive(list([solution[0]]), [index for index, _ in self.solutions], chosen, valid_points, xy_mat, (True, True))
            if t[1] == self.n:
                print('found max :(')
                return t
            if t[1] > max[1]:
                max = t
            elif t[1] == max[1]:
                max[0].extend(t[0])
        
        return max

    # @jit(forceobj=True)
    def choose_solution_recursive(self, chosen_solutions_ids: list[int], valid_solutions_ids: list[int], chosen_points: list[Point], valid_points: list[Point] = list(), valid_matrix: np.ndarray = np.zeros((0, 0)), options: tuple[bool] = tuple([True, True])):
        return 0

def __main__():
    n = 6
    grid = Grid(n=n, d=2)

    grid.find_max_solutions_2D()

    print('2D solutions:')
    for index, solution in grid.solutions:
        print(index, solution)
    
    start = timer()
    solutions = grid.order_2D_solutions(1, method='All')
    time = timer() - start
    print(time)
    grid.d = 3
    print(solutions)
    # points: list[Point] = list()
    # index = 0
    # for s in solutions[0][0]:
    #     bol = grid.solutions[s][1].copy()
    #     for i in range(bol.__len__()):
    #         bol[i].z = index
    #     points.extend(copy.deepcopy(bol))
    #     index = index + 1
        
    # print(points)
    # grid.points = points
    # grid.draw_grid()
    
__main__()