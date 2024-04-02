import random
from package.Point import Point
# from package.Grid import Grid

import itertools as it
import numpy as np
from math import gcd
from copy import deepcopy

class collision():
    amount: int = 0
    lines: list[list[Point]]
    
    def __init__(self) -> None:
        self.amount = 0
        self.lines = []
        
    def __eq__(self, __value: "collision") -> bool:
        return self.amount == __value.amount and self.lines == __value.lines

    def __str__(self):
        return str(self.amount)
    
    def __repr__(self) -> str:
        return str(self)

class GridPoints():
    idx_mat: np.ndarray
    collision_mat: np.ndarray[collision]
    chosen: list[Point]
    valid: list[Point]
    
    def __init__(self, n: int, d: int, k_in_line: int = 2): # O(n^d)
        self.idx_mat = np.full((n,) * d, fill_value=0, dtype=int)
        self.collision_mat = np.full((n,) * d, fill_value=None, dtype=collision)
        self.n = n
        self.d = d
        self.k = k_in_line
        self.valid = []
        self.chosen = []
        
        for cords in it.product(range(n), repeat=d):
            c = cords[::-1]
            self.valid.append(Point(*c, n=n))
            self.idx_mat[c] = -self.valid.__len__()
            self.collision_mat[c] = collision()
            
        self.chosen = []
            
    @classmethod
    def fromGrid(cls, grid):
        return cls(grid.n, grid.d) # calls init function
        
    def __len__(self):
        return self.chosen.__len__()
    
    def random_choice(self):
        return random.choice(self.chosen)
    
    def remove(self, point: Point, from_valid: bool = False): # O(d)
        mat_idx = tuple(point.cords)
        list_idx = abs(self.idx_mat[mat_idx]) - 1
        if list_idx < 0:
            raise IndexError()
        
        if from_valid:
            self.valid[list_idx] = self.valid[-1]
            list_idx = -list_idx - 1
            last_point = self.valid[-1]
        else:
            self.chosen[list_idx] = self.chosen[-1]
            list_idx += 1
            last_point = self.chosen[-1]
        self.idx_mat[tuple(last_point.cords)] = list_idx
        self.idx_mat[mat_idx] = 0
        
        if from_valid:
            self.valid.pop()
        else:
            self.chosen.pop()
        
    def __contains__(self, key: Point): # O(d)
        return self.idx_mat[tuple(key.cords)] > 0
    
    # append a point to the end of the list and update matrix
    def add_chosen(self, p: Point): # O(d)
        if p in self:
            return
        
        self.chosen.append(p)
        self.idx_mat[tuple(p.cords)] = self.chosen.__len__()
        
    def add(self, p: Point):
        if p in self:
            return
        
        self.removeInValidPoints([p], self.k)
        self.add_chosen(p)
    
    def __str__(self):
        return f'chosen: {self.chosen}\nvalid: {self.valid}\nidx_mat: \n{self.idx_mat}\ncollisions: \n{self.collision_mat}'
        # return 'chosen: ' + self.chosen + "\n" + 'valid: ' + self.valid + self.idx_mat
    
    def __repr__(self) -> str:
        return str(self)
    
    def __eq__(self, other: "GridPoints") -> bool:
        return np.all(self.idx_mat == other.idx_mat) and np.all(self.collision_mat == other.collision_mat) and self.chosen == other.chosen and self.valid == other.valid
    
    def __iter__(self):
        return iter(self.chosen)
    
    def sort(self):
        self.chosen.sort()
        i = 0
        for point in self.chosen:
            self.idx_mat[tuple(point.cords)] = i
            i += 1
        
    def removeInValidPoints(self, added_points: list[Point], k_in_line: int = 2):
        invalid_points: list[Point] = []
            
        if self.__len__() == 0:
            self.remove(added_points[-1], from_valid=True)
            self.add_chosen(added_points.pop())
            
            
        for added_point in added_points:
            if self.idx_mat[tuple(added_point.cords)] == 0:
                slot: collision = self.collision_mat[tuple(added_point.cords)]
                for line in slot.lines:
                    for point in line:
                        s: collision = self.collision_mat[tuple(point.cords)]
                        s.amount += 1
                
                # slot.amount += 1
                # slot.lines.append(line)
            
        for chosen_point in self:
            for added_point in added_points:
                d = chosen_point - added_point
                d = d // gcd(*(d.cords))
                
                line = [chosen_point, added_point]
                
                # collision for all points in line, always(not sure if its right to do this way)
                # for point in line:
                #     slot: collision = self.collision_mat[tuple(point.cords)]
                #     slot.amount += 1
                #     slot.lines.append(line)
                
                on_line = 1
                point = added_point + d
                while (point.max_cord() < self.n and point.min_cord() >= 0):
                    if point in self or point in added_points:
                        on_line += 1
                    else:
                        invalid_points.append(point)
                    point = point + d
                        
                    
                point = added_point - d
                while(point.max_cord() < self.n and point.min_cord() >= 0):
                    if point in self or point in added_points:
                        on_line += 1
                    else:
                        invalid_points.append(point)
                    point = point - d
                    
                if on_line >= k_in_line:
                    for point in invalid_points:
                        try:
                            slot: collision = self.collision_mat[tuple(point.cords)]
                            slot.amount += 1
                            slot.lines.append(line)
                            self.remove(point, from_valid=True)
                        except IndexError:
                            pass
                invalid_points = []
        
        for point in added_points:
            try:
                self.remove(point, from_valid=True)
            except IndexError:
                pass