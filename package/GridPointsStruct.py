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
            
    def add(self, p: Point): # O(1)
        if p in self:
            return
        
        self.removeInValidPoints(p)
        
        self.append_chosen(p)
        conflicts = np.where(np.logical_and(self.collision_mat > 0, self.idx_mat > 0))
        self.conflicted = []
        if len(conflicts[0]) == 0:
            return
        
        for i in range(len(conflicts[0])):
            # for j in range(len(conflicts[i])):
                # point = Point(*conflicts[i][j], n=self.n)
            point_coords = tuple([conflicts[j][i] for j in range(len(conflicts))])
            self.conflicted.append(Point(*point_coords, n=self.n))
            # point = Point(*conflicts[::-1][i], n=self.n)
        
        
    def append_chosen(self, p: Point): # O(1)
        if p in self:
            return
        
        self.chosen.append(p)
        self.idx_mat[tuple(p.coords)] = self.chosen.__len__()
        
    def append_valid(self, p: Point): # O(1)
        c = tuple(p.coords)
        if self.idx_mat[c] < 0:
            return
        
        self.valid.append(p)
        self.idx_mat[c] = -self.valid.__len__()
        
    def remove(self, p: Point):
        mat_idx = tuple(p.coords)
        list_idx = self.idx_mat[mat_idx] - 1
        
        self.recover(p)
        self.chosen[list_idx] = self.chosen[-1]
        list_idx += 1
        last_point = self.chosen[-1]
        self.idx_mat[tuple(last_point.coords)] = list_idx
        self.idx_mat[mat_idx] = 0
        
    def remove_chosen(self, p: Point):
        mat_idx = tuple(p.coords)
        hashed_list_index = self.idx_mat[mat_idx]
        if hashed_list_index <= 0:
            raise ValueError("Point is not chosen")
        actual_list_idx = hashed_list_index - 1
        
        self.chosen[actual_list_idx] = self.chosen[-1]
        
        last_point = self.chosen[-1]
        hashed_list_index = actual_list_idx + 1
        
        self.idx_mat[tuple(last_point.coords)] = hashed_list_index
        self.idx_mat[mat_idx] = 0
        
        self.chosen.pop()
        
    def remove_valid(self, p: Point):
        mat_idx = tuple(p.coords)
        hashed_list_index = self.idx_mat[mat_idx]
        if hashed_list_index >= 0:
            raise ValueError("Point is not valid")
        actual_list_idx = abs(hashed_list_index) - 1
        
        self.valid[actual_list_idx] = self.valid[-1]
        
        last_point = self.valid[-1]
        hashed_list_index = -(actual_list_idx + 1)
        
        self.idx_mat[tuple(last_point.coords)] = hashed_list_index
        self.idx_mat[mat_idx] = 0
        
        self.valid.pop()
        
        
    def recover(self, p: Point):
        
        lines = self.get_all_lines(p)

        for line, effected in lines:
            for effected_point in effected:
                self.remove_collision(p, effected_point)
  
    
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
            self.recover(point)
            self.chosen[list_idx] = self.chosen[-1]
            list_idx += 1
            last_point = self.chosen[-1]
        self.idx_mat[tuple(last_point.coords)] = list_idx
        self.idx_mat[mat_idx] = 0
        
        if from_valid:
            self.valid.pop()
        else:
            self.chosen.pop()
            
    # def recover(self, p: Point):
    #     suspects = np.where(self.collision_mat >= 0)
    #     for j in range(len(suspects[0])):
    #         suspect_point = tuple([suspects[k][j] for k in range(self.d)])
    #         slot: collision = self.collision_mat[suspect_point]
    #         i = 0
    #         while i < len(slot.lines):
    #             if p in slot.lines[i]:
    #                 slot.lines.pop(i)
    #                 slot.amount -= 1
    #                 i -= 1
    #             i += 1

                     
    def add(self, p: Point):
        if p in self:
            return
        
        self.removeInValidPoints(p)
        
        self.append_chosen(p)
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
            
    def get_line(self, p1: Point, p2: Point):
        chosen_line: list[Point] = []
        valid_line: list[Point] = []
        
        d = p1 - p2
        d = d // gcd(*tuple(d.coords))
        
        point = p1 + d
        while (point.max_cord() < self.n and point.min_cord() >= 0):
            is_chosen = point in self
            if is_chosen and point != p2:
                chosen_line.append(point)
            elif not is_chosen and point != p2:
                valid_line.append(point)
            point = point + d 
            
        point = p1 - d
        while(point.max_cord() < self.n and point.min_cord() >= 0):
            is_chosen = point in self
            if is_chosen and point != p2:
                chosen_line.append(point)
            elif not is_chosen and point != p2:
                valid_line.append(point)
            point = point - d
        
        return chosen_line, valid_line
        
    # O(k(n^d))
    def removeInValidPoints(self, added_point: Point):

        lines = self.get_all_lines(added_point) # O(k(n^d))

        added_loc = self.idx_mat[tuple(added_point.coords)]
        if added_loc < 0:
            self.remove_valid(added_point)

        for line, effected in lines: # O(n^(d-1))
            for effected_point in effected: # O(n - k)
                c = tuple(effected_point.coords)
                if self.idx_mat[c] < 0:
                    self.remove_valid(effected_point)
                self.add_collision(added_point, line)


    # def removeInValidPoints(self, added_point: Point):
            
    #     if len(self.chosen) == 0:
    #         self.remove_valid(added_point)
    #         self.append_chosen(added_point)
    #         return
            
    #     for chosen_point in self.chosen:
    #         chosen_line, valid_line = self.get_line(chosen_point, added_point)
                
    #         if len(chosen_line) >= self.k - 2:
    #             lines = list(list(line) for line in it.combinations(chosen_line, max(self.k - 2, 1)))
                
    #             for i in range(len(lines)):
    #                 lines[i].append(added_point)
    #                 if len(chosen_line) > self.k - 2:
    #                     self.add_collision(chosen_point, lines[i].copy())
    #                 lines[i].append(chosen_point)
                    
    #             if self.k == 2:
    #                 lines = [[added_point, chosen_point]]
                
    #             for point in valid_line:
    #                 try:
    #                     for line in lines:
    #                         self.add_collision(point, line)
    #                     self.remove(point, from_valid=True)
    #                 except IndexError:
    #                     pass
        
    #     try:  
    #         self.remove(added_point, from_valid=True)
    #     except:
    #         pass
        
    def get_all_lines(self, added: Point) -> list[tuple[list[Point], list[Point]]]:
        all_lines = []
        
        point_queue = self.chosen.copy()
        # O(k(n^d))
        while len(point_queue) > 0: # O(n^(d-1))
            chosen_line: list[Point] = []
            others_line: list[Point] = []
            
            context = point_queue[0]
            if context == added:
                continue
            d = added - context
            d = d // gcd(*tuple(d.coords))
            chosen_line.append(context)
            
            # build line: O(n)
            point = added + d
            while (point.max_cord() < self.n and point.min_cord() >= 0):
                is_chosen = point in self
                if is_chosen and point != context:
                    chosen_line.append(point)
                elif not is_chosen and point != context:
                    others_line.append(point)
                point = point + d 
                
            point = added - d
            while(point.max_cord() < self.n and point.min_cord() >= 0):
                is_chosen = point in self
                if is_chosen and point != context:
                    chosen_line.append(point)
                elif not is_chosen and point != context:
                    others_line.append(point)
                point = point - d
                
            # O(k^2)
            for point in chosen_line: # O(k)
                point_queue.remove(point) # O(k)
                
            if len(chosen_line) >= self.k - 1:
                
                # O(nk)
                for line in it.combinations(chosen_line, self.k - 1): # O(k)
                    line_set = set(line) # O(k)
                    line_list = list(line) # O(k)
                    
                    effected_list = [x for x in chosen_line if x not in line_set] + [x for x in others_line] # O(n)

                    line_list.append(added)
                    
                    all_lines.append((line_list, effected_list))
            
        
        return all_lines
        
    def add_collision(self, p: Point, line: list[Point]):
        slot: collision = self.collision_mat[tuple(p.coords)]
        slot.amount += 1
        slot.lines.append(line)

    def remove_collision(self, for_point: Point, with_point: Point):
        slot: collision = self.collision_mat[tuple(for_point.coords)]
        slot.amount -= 1
        i = 0
        while i < len(slot.lines):
            had_collision = True
            if with_point in slot.lines[i]:
                slot.lines.pop(i)
                i -= 1
            i += 1
        if len(slot.lines) == 0 and had_collision:
            self.append_valid(for_point)

        
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