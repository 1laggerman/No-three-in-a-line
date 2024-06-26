import matplotlib.pyplot as plt
import numpy as np
import itertools as it
from copy import deepcopy
import math
import random
from multiprocessing import Process
from package.Point import Point as Point
from package.GridPointsStruct import GridPoints
from package.collision import collision
import tqdm

class Grid:
    points: list[Point] = list()
    n = 1
    d = 2
    upper_bound: int
    solutions: list[tuple[int, list[Point]]]
    
    def __init__(self, n: int = 3, d: int = 2):
        self.n = n
        self.d = d
        self.upper_bound = math.pow(n, d-1)
        
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
    
    def random_greedy(self, sorted: bool = False, allowed_in_line: int = 2, start_from: GridPoints = None, show_progress: bool = False):
        gp: GridPoints = None
        if start_from is None:
            gp = GridPoints.fromGrid(self, k_in_line=allowed_in_line)
        else:
            gp = start_from
        
        while(len(gp.valid) != 0):
            added_point = random.choice(gp.valid)
            gp.add(added_point)
        
        if sorted:
            gp.sort()
        
        return gp
        
    def min_conflict(self, max_iter: int = 100, sorted: bool = True, allowed_in_line: int = 2, start_from: GridPoints = None, show_progress: bool = True):
        gp: GridPoints = None
        if start_from is None:
            gp = GridPoints.fromGrid(self, k_in_line=allowed_in_line)
        else:
            gp = start_from
        
        if allowed_in_line > self.n:
            allowed_in_line = self.n
        vectorized_func = np.vectorize(collision.num)
            
        progress_bar = tqdm.tqdm(total=max_iter, leave=False, desc='iters without new point') if show_progress else NoOpProgressBar()
        best_state = deepcopy(gp)
        # iters = []
        i = 0
        
        # with tqdm.tqdm(total=max_iter, position=1, leave=False) as bar:
        with progress_bar as bar:
            while i < max_iter and len(gp.chosen) < allowed_in_line * self.upper_bound:
                collision_count = vectorized_func(gp.collision_mat)
                
                # new valid point: collision_count = 0 and idx_mat <= 0
                legal_collision = gp.idx_mat <= 0
                collisions = np.logical_and(collision_count >= 0, legal_collision)
                min_conflict_value = np.min(np.where(collisions, collision_count, np.inf))
                min_conflict_points: np.ndarray = np.logical_and(collision_count == min_conflict_value, legal_collision)
                
                added_point = self.choose(min_conflict_points)
                
                gp.add(added_point)
                
                if len(gp.conflicted) == 0 or min_conflict_value == 0:
                    best_state = deepcopy(gp)
                    # iters.append(i)
                    bar.update(-i)
                    i = 0
                else:
                    c = random.choice(gp.conflicted)
                    gp.remove(c)
                    bar.update(1)
                    i += 1
        
        if sorted:
            gp.sort()
        # plt.plot(iters)
        # plt.show()
        return best_state
    
    def circular_build(self):
        C = np.zeros(self.d * self.n**2, dtype=int)
        for point in np.ndindex(*(self.n,) * self.d):
            i_x = sum((x+1)**2 for x in point)
            C[i_x] += 1
        return np.max(C)
        
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
    # def draw_grid(self, solutionID: list[int] = [-1], axis: str ='off', draw=True):
    #     ticks = np.arange(0, self.n, 1)
    #     fig = plt.figure(figsize=(12, 10), dpi=80)
    #     if self.d == 2:
    #         ax = plt.axes()
    #     elif self.d == 3:
    #         ax = plt.axes(projection='3d')
    #         ax.set_zticks(ticks)
    #         ax.set_zlim(0, self.n - 1)
            
    #     ax.set_xticks(ticks)
    #     ax.set_yticks(ticks)
    #     # ax.set_xlim(-0.1, self.n - 0.9)
    #     # ax.set_ylim(-0.1, self.n - 0.9)
        
        
    #     if self.d == 2:
    #         for x in range(self.n):
    #             ax.plot([x, x], [0, self.n - 1], 'grey')
    #         for y in range(self.n):
    #             ax.plot([0, self.n - 1], [y, y], 'grey')

    #         for point in self.points:
    #             ax.scatter([point.coords[0]], [point.coords[1]], s=500, c='r', edgecolor='black', linewidth=2)	
    #         if solutionID != [-1]:
    #             for point in self.solutions[solutionID[0]]:
    #                 ax.scatter([point.x], [point.y], color='black', s=250)
            
    #     elif self.d == 3:
    #         # paint grid lines:
            
    #         # paint X-lines:
    #         for y in range(self.n):
    #             for z in range(self.n):
    #                 ax.plot3D([0, self.n - 1], [y, y], [z, z], 'grey')
            
    #         # paint Y-lines:
    #         for x in range(self.n):
    #             for z in range(self.n):
    #                 ax.plot3D([x, x], [0, self.n - 1], [z, z], 'grey')
            
    #         # paint Z-lines:
    #         for x in range(self.n):
    #             for y in range(self.n):
    #                 ax.plot3D([x, x], [y, y], [0, self.n - 1], 'grey')        

    #         # paint lines from (0, 0 ,0) to visualize directions:
    #         ax.plot3D([0, self.n - 1], [0, 0], [0, 0], 'red') # paint red to visualize X axis
    #         ax.plot3D([0, 0], [0, self.n - 1], [0, 0], 'green') # green to visualize Y axis
    #         ax.plot3D([0, 0], [0, 0], [0, self.n - 1], 'blue') # blue to visualize Z axis
            
    #         for point in self.points: # paint all dots on grid
    #             ax.scatter([point.coords[0]], [point.coords[1]], [point.coords[2]], color='black', s=250)
    #         if solutionID[0] != -1:
    #             z = 0
    #             for s in solutionID:
    #                 for point in self.solutions[s][1]:
    #                     ax.scatter([point.x], [point.y], [z], color='black', s=250)
    #                 z = z + 1
            
    #     else:
    #         print('figure cannot be shown for %d dimentions'.format(self.d))
            
    #     if axis == 'off':
    #         plt.axis('off')
    #     else:
    #         ax.set_xlabel('X axis')
    #         ax.set_ylabel('Y axis')
    #         if self.d == 3:
    #             ax.set_zlabel('Z axis')
            
    #     # manager = plt.get_current_fig_manager()
    #     # manager.full_screen_toggle()
    #     # ax.margins(0.02)
    #     plt.show()
    
    def draw_grid(self, solutionID: list[int] = [-1], axis: str ='off'):
        ax = self.make_grid(solutionID, axis)
        plt.show()
        
    # def make_grid(self, solutionID: list[int] = [-1], axis: str ='off'):
        # ticks = np.arange(0, self.n, 1)
        # fig, ax = plt.subplots(figsize=(12, 10), dpi=80, subplot_kw={'projection': '3d'} if self.d == 3 else None)

        # ax.set_xticks(ticks)
        # ax.set_yticks(ticks)
        # if self.d == 3:
        #     ax.set_zticks(ticks)
        #     ax.set_zlim(0, self.n - 1)

        # if self.d == 2:
        #     self.plot_2d_grid(ax, solutionID)
        # elif self.d == 3:
        #     self.plot_3d_grid(ax, solutionID)
        # else:
        #     print(f'Grid cannot be shown for {self.d} dimensions')

        # if axis == 'off':
        #     ax.axis('off')
        # else:
        #     ax.set_xlabel('X axis')
        #     ax.set_ylabel('Y axis')
        #     if self.d == 3:
        #         ax.set_zlabel('Z axis')

        # return ax  # Return the Axes object instead of showing it
        
    def make_grid(self, ax, solution: GridPoints = None, axis: str ='off'):
        ticks = np.arange(0, self.n, 1)
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        if self.d == 3:
            ax.set_zticks(ticks)
            ax.set_zlim(0, self.n - 1)

        if self.d == 2:
            self.plot_2d_grid(ax, solution)
        elif self.d == 3:
            self.plot_3d_grid(ax, solution)
        else:
            print(f'Grid cannot be shown for {self.d} dimensions')

        if axis == 'off':
            ax.axis('off')
        else:
            ax.set_xlabel('X axis')
            ax.set_ylabel('Y axis')
            if self.d == 3:
                ax.set_zlabel('Z axis')

    def plot_2d_grid(self, ax, solution: GridPoints):
        for x in range(self.n):
            ax.plot([x, x], [0, self.n - 1], 'grey')
        for y in range(self.n):
            ax.plot([0, self.n - 1], [y, y], 'grey')

        for point in self.points:
            ax.scatter([point.coords[0]], [point.coords[1]], s=500, c='r', edgecolor='black', linewidth=2)  
        if solution != None:
            for point in solution.chosen:
                ax.scatter([point.coords[0]], [point.coords[1]], color='black', s=250)

    def plot_3d_grid(self, ax, solution: GridPoints):
        # Paint grid lines for X, Y, and Z directions
        for y in range(self.n):
            for z in range(self.n):
                ax.plot3D([0, self.n - 1], [y, y], [z, z], 'grey')
        for x in range(self.n):
            for z in range(self.n):
                ax.plot3D([x, x], [0, self.n - 1], [z, z], 'grey')
        for x in range(self.n):
            for y in range(self.n):
                ax.plot3D([x, x], [y, y], [0, self.n - 1], 'grey')

        for point in self.points:
            ax.scatter([point.coords[0]], [point.coords[1]], [point.coords[2]], color='black', s=250)
        if solution != None:
            for point in solution.chosen:
                ax.scatter([point.coords[0]], [point.coords[1]], [point.coords[2]], color='black', s=250)
        
    def choose(self, condition: np.ndarray):
        choose_from = np.where(condition)
        point_idx = np.random.choice(range(len(choose_from[0])))
        point_coords = tuple([choose_from[i][point_idx] for i in range(self.d)])
        point = Point(*point_coords, n=self.n)
        
        return point 
    
class NoOpProgressBar:
    def update(self, n=1):
        pass

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()