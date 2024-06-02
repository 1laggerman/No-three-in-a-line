import random
from package.Point import Point
from package.collision import collision
# from package.Grid import Grid

import itertools as it
import numpy as np
from math import gcd
from copy import deepcopy

class GridPoints():
    idx_mat: np.ndarray
    chosen: list[Point]
    valid: list[Point]
    collision_mat: np.ndarray[collision]
    conflicted: list[Point]
    
    def __init__(self, n: int, d: int, k_in_line: int = 2): # O(n^d)
        self.idx_mat = np.full((n,) * d, fill_value=0, dtype=int)
        self.collision_mat = np.full((n,) * d, fill_value=None, dtype=collision)
        self.n = n
        self.d = d
        self.k = k_in_line
        self.valid = []
        self.chosen = []
        self.conflicted = []
        
        # add all valid points and initialize collision
        for cords in it.product(range(n), repeat=d):
            c = cords[::-1]
            self.valid.append(Point(*c, n=n))
            self.idx_mat[c] = -self.valid.__len__() 
            self.collision_mat[c] = collision()
            
    @classmethod
    def fromGrid(cls, grid, k_in_line: int = 2):
        return cls(grid.n, grid.d, k_in_line) # calls init function
    
    def sort(self):
        self.chosen.sort()
        self.valid.sort()
        i = 1
        for point in self.chosen:
            self.idx_mat[tuple(point.coords)] = i
            i += 1
            
        i = -1
        for point in self.valid:
            self.idx_mat[tuple(point.coords)] = i
            i -= 1
    
    def remove(self, point: Point, from_valid: bool = False): # O(d)
        mat_idx = tuple(point.coords)
        list_idx = abs(self.idx_mat[mat_idx]) - 1
        if list_idx < 0:
            raise IndexError()
        
        if from_valid:
            self.valid[list_idx] = self.valid[-1]
            list_idx = -list_idx - 1
            last_point = self.valid[-1]
        else:
            self.remove_chosen(point)
            self.chosen[list_idx] = self.chosen[-1]
            list_idx += 1
            last_point = self.chosen[-1]
        self.idx_mat[tuple(last_point.coords)] = list_idx
        self.idx_mat[mat_idx] = 0
        
        if from_valid:
            self.valid.pop()
        else:
            self.chosen.pop()
            
    def remove_chosen(self, p: Point):
        suspects = np.where(self.collision_mat >= 0)
        for j in range(len(suspects[0])):
            suspect_point = tuple([suspects[k][j] for k in range(self.d)])
            slot: collision = self.collision_mat[suspect_point]
            i = 0
            while i < len(slot.lines):
                if p in slot.lines[i]:
                    slot.lines.pop(i)
                    slot.amount -= 1
                    i -= 1
                i += 1
                        
    def add(self, p: Point):
        if p in self:
            return
        
        self.removeInValidPoints(p)
        
        self.add_chosen(p)
        conflicts = np.logical_and(self.collision_mat > 0, self.idx_mat > 0)
        conflicts = np.where(conflicts)
        self.conflicted = []
        if len(conflicts[0]) == 0:
            return
        
        for i in range(len(conflicts[0])):
            # for j in range(len(conflicts[i])):
                # point = Point(*conflicts[i][j], n=self.n)
            point_coords = tuple([conflicts[j][i] for j in range(len(conflicts))])
            self.conflicted.append(Point(*point_coords, n=self.n))
            # point = Point(*conflicts[::-1][i], n=self.n)

    # append a point to the end of the list and update matrix
    def add_chosen(self, p: Point): # O(d)
        if p in self:
            return
        
        self.chosen.append(p)
        self.idx_mat[tuple(p.coords)] = self.chosen.__len__()
            
    def get_line(self, p1: Point, p2: Point):
        chosen_line: list[Point] = []
        valid_line: list[Point] = []
        
        d = p1 - p2
        d = d // gcd(*(d.coords))
        
        point = p1 + d
        while (point.max_cord() < self.n and point.min_cord() >= 0):
            if point in self and point != p2:
                chosen_line.append(point)
            elif point not in self and point != p2:
                valid_line.append(point)
            point = point + d 
            
        point = p1 - d
        while(point.max_cord() < self.n and point.min_cord() >= 0):
            if point in self and point != p2:
                chosen_line.append(point)
            elif point not in self and point != p2:
                valid_line.append(point)
            point = point - d
        
        return chosen_line, valid_line
        
    def removeInValidPoints(self, added_point: Point):
            
        if self.__len__() == 0:
            self.remove(added_point, from_valid=True)
            self.add_chosen(added_point)
            return
            
        for chosen_point in self.chosen:
            chosen_line, valid_line = self.get_line(chosen_point, added_point)
                
            if len(chosen_line) >= self.k - 2:
                lines = list(list(line) for line in it.combinations(chosen_line, max(self.k - 2, 1)))
                
                for i in range(len(lines)):
                    lines[i].append(added_point)
                    if len(chosen_line) > self.k - 2:
                        self.add_collision(chosen_point, lines[i].copy())
                    lines[i].append(chosen_point)
                    
                if self.k == 2:
                    lines = [[added_point, chosen_point]]
                
                for point in valid_line:
                    try:
                        for line in lines:
                            self.add_collision(point, line)
                        self.remove(point, from_valid=True)
                    except IndexError:
                        pass
        
        try:  
            self.remove(added_point, from_valid=True)
        except:
            pass
        
    def add_collision(self, p: Point, line: list[Point]):
        slot: collision = self.collision_mat[tuple(p.coords)]
        slot.amount += 1
        slot.lines.append(line)
        
    def __contains__(self, key: Point): # O(d)
        return self.idx_mat[tuple(key.coords)] > 0
        
    def __len__(self):
        return self.chosen.__len__()
    
    def choose(self, condition: np.ndarray):
        choose_from = np.where(condition)
        point_idx = np.random.choice(choose_from[0])
        point_coords = tuple([choose_from[i][point_idx] for i in range(len(choose_from))])
        point = Point(*point_coords, n=self.n)
        return point 
    
    def __str__(self):
        return f'chosen: {self.chosen}\nvalid: {self.valid}\nidx_mat: \n{self.idx_mat}\ncollisions: \n{self.collision_mat}'
    
    def __repr__(self) -> str:
        return str(self)
    
    def __eq__(self, other: "GridPoints") -> bool:
        if other is None:
            return False
        return np.all(self.idx_mat == other.idx_mat) and np.all(self.collision_mat == other.collision_mat) and self.chosen == other.chosen and self.valid == other.valid
    
    def __iter__(self):
        return iter(self.chosen)