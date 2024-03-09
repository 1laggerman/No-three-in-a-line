import random
from .PointG import PointG as Point
# from .GridG import GridG as Grid

import numpy as np
import copy

class GridPoints():
    m: np.ndarray
    l: list[Point]
    
    def __init__(self, points: list[Point], n: int, d: int): # O(n * d)
        self.m = np.full((n,) * d, fill_value=-1, dtype=int)
        i = 0
        for point in points:
            self.m[tuple(point.cords)] = i
            i += 1
        
        self.l = copy.deepcopy(points)
            
    @classmethod
    def fromGrid(cls, points: list[Point], grid):
        return cls(points, grid.n, grid.d)
        
    def __len__(self):
        return self.l.__len__()
    
    def random_choice(self):
        return random.choice(self.l)
    
    def remove(self, point: Point): # O(d)
        mat_idx = tuple(point.cords)
        list_idx = self.m[mat_idx]
        if list_idx == -1:
            raise IndexError()
        
        self.m[mat_idx] = -1
        self.l[list_idx] = self.l[-1]
        self.m[tuple(self.l[-1].cords)] = list_idx
        self.l.pop()
        
    def __contains__(self, key: Point): # O(d)
        return self.l[self.m[tuple(key.cords)]] == key
    
    def append(self, __other: Point): # O(d)
        if __other in self:
            return
        self.m[tuple(__other.cords)] = self.l.__le__()
        self.l.append(__other)
    
    def __str__(self):
        return self.l.__str__() + "\n" + self.m.__str__()
    
    def __repr__(self) -> str:
        return str(self)
    
    def __eq__(self, __value: "GridPoints") -> bool:
        return np.all(self.m == __value.m)
    
    def __iter__(self):
        return iter(self.l)
    