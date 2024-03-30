import random
from package.Point import Point
# from package.Grid import Grid

import itertools as it
import numpy as np
from math import gcd
from typing import Any

class GridPoints():
    idx_mat: np.ndarray
    collision_mat: np.ndarray
    chosen: list[Point]
    valid: list[Point]
    
    def __init__(self, n: int, d: int): # O(n^d)
        self.idx_mat = np.full((n,) * d, fill_value=-1, dtype=int)
        self.collision_mat = np.full((n,) * d, fill_value=[], dtype=object)
        
        for cords in it.product(range(n), repeat=d):
            self.valid.append(Point(*reversed(cords), n=n))
        
        self.chosen = []
            
    @classmethod
    def fromGrid(cls, grid):
        return cls(grid.n, grid.d) # calls init function
        
    def __len__(self):
        return self.chosen.__len__()
    
    def random_choice(self):
        return random.choice(self.chosen)
    
    def remove(self, point: Point): # O(d)
        mat_idx = tuple(point.cords)
        list_idx = self.idx_mat[mat_idx] - 1
        if list_idx < 0:
            raise IndexError()
        
        self.chosen[list_idx] = self.chosen[-1]
        self.idx_mat[tuple(self.chosen[-1].cords)] = list_idx
        self.idx_mat[mat_idx] = 0
        self.chosen.pop()
        
    def __contains__(self, key: Point): # O(d)
        return self.idx_mat[tuple(key.cords)] > 0
    
    # append a point to the end of the list and update matrix
    def append(self, p: Point): # O(d)
        if p in self:
            return
        self.idx_mat[tuple(p.cords)] = self.chosen.__len__()
        self.chosen.append(p)
        
    # append and update matrix with collisions
    def add_collision(self, location: Point): # O(d)
        if location in self:
            return
        self.idx_mat[tuple(location.cords)] -= 1
    
    def __str__(self):
        return self.chosen.__str__() + "\n" + self.idx_mat.__str__()
    
    def __repr__(self) -> str:
        return str(self)
    
    def __eq__(self, __value: "GridPoints") -> bool:
        return np.all(self.idx_mat == __value.idx_mat)
    
    def __iter__(self):
        return iter(self.chosen)
    
    def sort(self):
        self.chosen.sort()
        i = 0
        for point in self.chosen:
            self.idx_mat[tuple(point.cords)] = i
            i += 1
        
    def removeInValidPoints(self, added_points: list[Point], valid_points: "GridPoints", k_in_line: int = 2):
        invalid_points = GridPoints.fromGrid([], self)
            
        if self.__len__() == 0:
            self.append(added_points[-1])
            valid_points.remove(added_points.pop())
            
        added = GridPoints.fromGrid(added_points, self)
        for chosen_point in self:
            for added_point in added:
                d = chosen_point - added_point
                d = d // gcd(*(d.cords))
                
                on_line = 1
                point = added_point + d
                while (point.max_cord() < self.n and point.min_cord() >= 0):
                    if point in self or point in added:
                        on_line += 1
                    else:
                        invalid_points.append(point)
                    point = point + d
                        
                    
                point = added_point - d
                while(point.max_cord() < self.n and point.min_cord() >= 0):
                    if point in self or point in added:
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