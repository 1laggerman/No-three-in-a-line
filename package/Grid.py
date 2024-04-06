import matplotlib.pyplot as plt
import numpy as np
import itertools as it
from copy import deepcopy
import math
import random
from multiprocessing import Process
from package.Point import Point as Point
from package.GridPointsStruct import GridPoints

class Grid:
    points: list[Point] = list()
    n = 1
    d = 2
    solutions: list[tuple[int, list[Point]]]
    
    def __init__(self, n: int = 3, d: int = 2):
        self.n = n
        self.d = d
        
    def add_point(self, p: Point):
        padding = max(0, self.n - p.coords.__len__())
        self.points.append(Point(*np.pad(p.coords, (0, padding), mode='constant'), n=self.n))
        
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
        ValidPoints: list[Point] = list()
        if d < 0:
            d = self.d    
        for cords in it.product(range(self.n), repeat=d):
            ValidPoints.append(Point(*reversed(cords), n=self.n))
                                
        return ValidPoints
    
    def removeInValidPoints(self, added_points: list[Point], valid_points: GridPoints, chosen_points: GridPoints = None, k_in_line: int = 2):
        invalid_points = GridPoints.fromGrid([], self)
        
        chosen = chosen_points
        if chosen_points is None:
            chosen = GridPoints.fromGrid([], self)
            
        if chosen_points.__len__() == 0:
            chosen.append(added_points[-1])
            valid_points.remove(added_points.pop())
            
        added = GridPoints.fromGrid(added_points, self)
        for chosen_point in chosen:
            for added_point in added:
                d = chosen_point - added_point
                d = d // math.gcd(*(d.cords))
                
                on_line = 1
                point = added_point + d
                while (point.max_cord() < self.n and point.min_cord() >= 0):
                    if point in chosen or point in added:
                        on_line += 1
                    else:
                        invalid_points.append(point)
                    point = point + d
                        
                    
                point = added_point - d
                while(point.max_cord() < self.n and point.min_cord() >= 0):
                    if point in chosen or point in added:
                        on_line += 1
                    else:
                        invalid_points.append(point)
                    point = point - d
                    
                if on_line >= k_in_line:
                    for point in invalid_points:
                        try:
                            valid_points.remove(point)
                        except IndexError:
                            pass
                invalid_points = []
        
        for point in added:
            try:
                valid_points.remove(point)
            except IndexError:
                pass
                
        
        return valid_points
    
    
    def random_greedy(self, sorted: bool = False, allowed_in_line: int = 2):
        valid_points = GridPoints.fromGrid(self.getAllValidPoints(), self)
        
        chosen_points: GridPoints = GridPoints.fromGrid([], self)
        while(valid_points.__len__() != 0):
            added_point = valid_points.random_choice()
            valid_points = self.removeInValidPoints([added_point], valid_points, chosen_points, k_in_line=allowed_in_line)
            chosen_points.append(added_point)
        if sorted:
            chosen_points.sort()
        return (chosen_points, chosen_points.__len__())
        
    def min_conflict(self, max_iter: int = 1000, sorted: bool = True, allowed_in_line: int = 2):
        gp: GridPoints = GridPoints.fromGrid([], k_in_line=allowed_in_line)
        while(len(gp.valid) != 0):
            added_point = gp.random_choice()
            gp.add(added_point)
            
        best_state = deepcopy(gp)
        i = 0    
        while i < max_iter:
            min_conflict_point = Point(*np.unravel_index(np.argmin(gp.collision_mat), gp.collision_mat.shape), n=self.n)
            gp.add(min_conflict_point)
            if len(gp.conflicted) == 0:
                best_state = deepcopy(gp)
            else:
                random.choice(gp.conflicted)
            i += 1
        
        if sorted:
            gp.sort()
        return (best_state.chosen, len(best_state.chosen))

        
    def __str__(self):
        gridStr = '['
        i = 0
        while i < self.points.__len__() - 1:
            gridStr += self.points[i].__str__() + ', '
            i = i + 1
        if self.points.__len__() > 0:
            gridStr += self.points[-1].__str__()
        gridStr += ']'
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