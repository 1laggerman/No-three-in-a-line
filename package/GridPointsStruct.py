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
        
        # add all valid points and initialize collision
        for cords in it.product(range(n), repeat=d):
            c = cords[::-1]
            self.valid.append(Point(*c, n=n))
            self.idx_mat[c] = -self.valid.__len__() 
            self.collision_mat[c] = collision()
            
    @classmethod
    def fromGrid(cls, grid):
        return cls(grid.n, grid.d) # calls init function
        
    def __len__(self):
        return self.chosen.__len__()
    
    def random_choice(self):
        return random.choice(self.chosen)
    
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
            self.chosen[list_idx] = self.chosen[-1]
            list_idx += 1
            last_point = self.chosen[-1]
        self.idx_mat[tuple(last_point.coords)] = list_idx
        self.idx_mat[mat_idx] = 0
        
        if from_valid:
            self.valid.pop()
        else:
            self.chosen.pop()
        
    def __contains__(self, key: Point): # O(d)
        return self.idx_mat[tuple(key.coords)] > 0
    
    # append a point to the end of the list and update matrix
    def add_chosen(self, p: Point): # O(d)
        if p in self:
            return
        
        self.chosen.append(p)
        self.idx_mat[tuple(p.coords)] = self.chosen.__len__()
        
    def add(self, p: Point):
        if p in self:
            return
        
        self.removeInValidPoints(p, self.k)
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
            self.idx_mat[tuple(point.coords)] = i
            i += 1
            
            
    def get_line_lines(self, p1: Point, p2: Point, k: int = 2):
        lines: list[list[Point]] = []
        chosen = self.chosen.copy()
        
        while chosen.__len__() > 0:
            chosen_point = chosen[0]
            if chosen_point == p1 or chosen_point == p2:
                chosen.remove(chosen_point)
            else:
                d = p1 - p2
                d = d // gcd(*(d.coords))
                
                line = []
                
                point = p1 + d
                while (point.max_cord() < self.n and point.min_cord() >= 0):
                    if point in self and point != p2:
                        line.append(point)
                    point = point + d 
                    
                point = p1 - d
                while(point.max_cord() < self.n and point.min_cord() >= 0):
                    if point in self and point != p2:
                        line.append(point)
                    point = point - d
                    
                if line.__len__() >= k - 2:
                    for k_line in it.combinations(line, k):
                        lines.append(list(k_line))
                        
                for point in line:
                    chosen.remove(point)
            
        return lines
            
    def get_point_lines(self, p: Point, k: int = 2):
        lines: list[list[Point]] = []
        chosen = self.chosen.copy()
        
        while chosen.__len__() > 0:
            chosen_point = chosen[0]
            if chosen_point == p:
                chosen.remove(chosen_point)
            else:
                d = chosen_point - p
                d = d // gcd(*(d.coords))
                
                line = []
                
                point = p + d
                while (point.max_cord() < self.n and point.min_cord() >= 0):
                    if point in self:
                        line.append(point)
                    point = point + d 
                    
                point = p - d
                while(point.max_cord() < self.n and point.min_cord() >= 0):
                    if point in self:
                        line.append(point)
                    point = point - d
                    
                if line.__len__() >= k_line - 1:
                    for k_line in it.combinations(line, k):
                        lines.append(list(k_line))
                        
                for point in line:
                    chosen.remove(point)
            
        return lines
        
    def removeInValidPoints(self, added_point: Point, k_in_line: int = 2):
        invalid_points: list[Point] = []
        chosen: list[Point] = self.chosen.copy()
            
        if self.__len__() == 0:
            self.remove(added_point, from_valid=True)
            self.add_chosen(added_point)
            return
            
            
        # if self.idx_mat[tuple(added_point.coords)] == 0:
        #     slot: collision = self.collision_mat[tuple(added_point.coords)]
        #     for line in slot.lines:
        #         for point in line:
        #             s: collision = self.collision_mat[tuple(point.coords)]
        #             s.amount += 1
        for chosen_point in chosen:
            d = chosen_point - added_point
            d = d // gcd(*(d.coords))
            
            line = []
            
            point = added_point + d
            while (point.max_cord() < self.n and point.min_cord() >= 0):
                if point in self and point != chosen_point:
                    line.append(point)
                elif point not in self:
                    invalid_points.append(point)
                point = point + d
                    
                
            point = added_point - d
            while(point.max_cord() < self.n and point.min_cord() >= 0):
                if point in self and point != chosen_point:
                    line.append(point)
                elif point not in self:
                    invalid_points.append(point)
                point = point - d
                
            if line.__len__() >= k_in_line - 2:
                lines = list(list(line) for line in it.combinations(line, max(k_in_line - 2, 1)))
                
                for i in range(lines.__len__()):
                    lines[i].append(added_point)
                    if line.__len__() > k_in_line - 2:
                        self.add_collision(chosen_point, lines[i].copy())
                    lines[i].append(chosen_point)
                    
                if k_in_line == 2:
                    lines = [[added_point, chosen_point]]
                
                for point in invalid_points:
                    try:
                        for line in lines:
                            self.add_collision(point, line)
                        self.remove(point, from_valid=True)
                    except IndexError:
                        pass
                    
                # elif line.__len__() > k_in_line:
                #     for point in invalid_points:
                #         slot: collision = self.collision_mat[tuple(point.coords)]
                #         slot.amount += 1
                #         slot.lines.append(line)
                        # for 
                
                # point = added_point + d
                # while (point.max_cord() < self.n and point.min_cord() >= 0):
                #     if point in self or point in added_points:
                #         on_line += 1
                #         line.append(point)
                #     else:
                #         invalid_points.append(point)
                #     point = point + d
                        
                    
                # point = added_point - d
                # while(point.max_cord() < self.n and point.min_cord() >= 0):
                #     if point in self or point in added_points:
                #         on_line += 1
                #     else:
                #         invalid_points.append(point)
                #     point = point - d
                    
                # if on_line >= k_in_line:
                #     for point in invalid_points:
                #         try:
                #             slot: collision = self.collision_mat[tuple(point.coords)]
                #             slot.amount += 1
                #             slot.lines.append(line)
                #             self.remove(point, from_valid=True)
                #         except IndexError:
                #             pass
                
            invalid_points = []
            
        try:
            self.remove(point, from_valid=True)
        except IndexError:
            pass
        
    def add_collision(self, p: Point, line: list[Point]):
        slot: collision = self.collision_mat[tuple(p.coords)]
        slot.amount += 1
        slot.lines.append(line)