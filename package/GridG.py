import matplotlib.pyplot as plt
import numpy as np
import itertools as it
import copy
import math
import random
from .PointG import PointG as Point

# from numba import jit, cuda
from multiprocessing import Process

class GridG:
    points: list[Point] = list()
    n = 1
    d = 2
    solutions: list[tuple[int, list[Point]]]
    
    def __init__(self, n: int = 3, d: int = 2):
        self.n = n
        self.d = d
        
    def add_point(self, p: Point):
        padding = max(0, self.n - p.cords.__len__())
        self.points.append(Point(*np.pad(p.cords, (0, padding), mode='constant'), n=self.n))
        
    def add_points(self, points_arr: list):
        for point in points_arr:
            self.points.append(point)
            
    def is_solution(self, points: list[Point]):
        points.extend(self.points)
        
        for point1, point2, point3 in it.combinations(points, 3):
            if point1.onTheSameLine(point2, point3):
                return False
        return True
    
    def getAllValidPoints(self, d: int = -1, chosen: list = list()):
        chosen.extend(self.points)
        ValidPoints: set[Point] = set()
        if d < 0:
            d = self.d    
        for cords in it.product(range(self.n), repeat=d):
            ValidPoints.add(Point(*reversed(cords), n=self.n))
                                
        return ValidPoints
    
    def removeInValidPoints(self, added_points: list[Point], valid_points: list[Point], chosen_points: list[Point] = list()):
        invalid_points = set()
        chosen = []
        
        if chosen_points.__len__() == 0:
            chosen.append(added_points[0])
            added_points.pop(0)
        else:
            chosen = chosen_points
        
        for chosen_point in chosen:
            for added_point in added_points:
                d = chosen_point - added_point
                d = d / math.gcd(*(d.cords))
                point = added_point
                while (point.max_cord() < self.n and point.min_cord() >= 0):
                    invalid_points.add(point)
                    point = point + d
                point = added_point - d
                while(point.max_cord() < self.n and point.min_cord() >= 0):
                    invalid_points.add(point)
                    point = point - d
                    
        valid_points = [x for x in valid_points if x not in invalid_points]
        return valid_points
    
    
    def random_greedy(self):
        valid_points = self.getAllValidPoints()
        chosen_points = []
        while(valid_points.__len__() != 0):
            added_point = random.choice(valid_points)
            valid_points = self.removeInValidPoints([added_point], valid_points, chosen_points)
            chosen_points.append(added_point)
        chosen_points.sort()
        return (chosen_points, chosen_points.__len__())
        
    
    def __str__(self):
        gridStr = '['
        i = 0
        while i < self.points.__len__() - 1:
            gridStr += self.points[i].__str__() + ', '
            i = i + 1
        gridStr += self.points[i].__str__() + ']'
        return gridStr         
            
        
    def print_grid_2D(self, solutionID: int = -1, mat: np.ndarray[int] = np.zeros((1, 1))):
        if mat.shape == (1, 1):
            mat = np.zeros((self.n, self.n), int)
            points_list = self.points
            if solutionID != -1:
                points_list = self.solutions[solutionID][1]
            for point in points_list:
                mat[point.x, point.y] = mat[point.x, point.y] + 1
            
        for i in range(self.n):
            print(mat[self.n - i - 1, :])
        
    # Grid functions:
    def draw_grid(self, solutionID: list[int] = [-1], axis: str ='off'):
        ticks = np.arange(0, self.n, 1)
        fig = plt.figure(figsize=(12, 10), dpi=80)
        if self.d == 2:
            ax = plt.axes()
        elif self.d == 3:
            ax = plt.axes(projection='3d')
            ax.set_zticks(ticks)
            ax.set_zlim(0, self.n - 1)
            
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        # ax.set_xlim(-0.1, self.n - 0.9)
        # ax.set_ylim(-0.1, self.n - 0.9)
        
        
        if self.d == 2:
            for x in range(self.n):
                ax.plot([x, x], [0, self.n - 1], 'grey')
            for y in range(self.n):
                ax.plot([0, self.n - 1], [y, y], 'grey')

            for point in self.points:
                ax.scatter([point.x], [point.y], color='black', s=250)
            if solutionID != -1:
                for point in self.solutions[solutionID]:
                    ax.scatter([point.x], [point.y], color='black', s=250)
            
        elif self.d == 3:
            # paint grid lines:
            
            # paint X-lines:
            for y in range(self.n):
                for z in range(self.n):
                    ax.plot3D([0, self.n - 1], [y, y], [z, z], 'grey')
            
            # paint Y-lines:
            for x in range(self.n):
                for z in range(self.n):
                    ax.plot3D([x, x], [0, self.n - 1], [z, z], 'grey')
            
            # paint Z-lines:
            for x in range(self.n):
                for y in range(self.n):
                    ax.plot3D([x, x], [y, y], [0, self.n - 1], 'grey')        

            # paint lines from (0, 0 ,0) to visualize directions:
            ax.plot3D([0, self.n - 1], [0, 0], [0, 0], 'red') # paint red to visualize X axis
            ax.plot3D([0, 0], [0, self.n - 1], [0, 0], 'green') # green to visualize Y axis
            ax.plot3D([0, 0], [0, 0], [0, self.n - 1], 'blue') # blue to visualize Z axis
            
            for point in self.points: # paint all dots on grid
                ax.scatter([point.x], [point.y], [point.z], color='black', s=250)
            if solutionID[0] != -1:
                z = 0
                for s in solutionID:
                    for point in self.solutions[s][1]:
                        ax.scatter([point.x], [point.y], [z], color='black', s=250)
                    z = z + 1
            
        else:
            print('figure cannot be shown for %d dimentions'.format(self.d))
            
        if axis == 'off':
            plt.axis('off')
        else:
            ax.set_xlabel('X axis')
            ax.set_ylabel('Y axis')
            if self.d == 3:
                ax.set_zlabel('Z axis')
            
        # manager = plt.get_current_fig_manager()
        # manager.full_screen_toggle()
        # ax.margins(0.02)
        plt.show()
        
def union_solutions(set1: list[Point], set2: list[Point], length: int):
    for solution1 in set1:
        for solution2 in set2:
            i = 0
            while i < length and solution1[i] == solution2[i]:
                i = i + 1
            if i == length:
                set2.remove(solution2)
        
    # add all valid solutions:
    set1.extend(set2)