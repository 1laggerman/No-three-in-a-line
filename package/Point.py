import numpy as np

class Point:
    coords: np.ndarray
    n: int
    
    def __init__(self, *coordinates: int, n: int = 3):
        self.coords = np.array([x for x in coordinates])
        self.n = n # max value of coordinates, for hashing porposes
        
    def __str__(self) -> str:
        pointStr = '('
        i = 0
        while i < self.coords.__len__() - 1:
            pointStr += f'{self.coords[i]}, '
            i = i + 1
        pointStr += f'{self.coords[i]})'
        return pointStr
    
    def __repr__(self):
        return str(self)
        
    def __add__(self, __other: "Point"):
        return Point(*(self.coords + __other.coords))
    
    def mul(self, __other: "Point"):
        return Point(*(self.coords * __other.coords))
    
    def __matmul___(self, __other: "Point"):
        return self.coords @ __other.coords
        
    def __truediv__(self, scalar):
        return Point(*(self.coords / scalar))
    
    def __floordiv__(self, scalar):
        return Point(*(self.coords // scalar))
    
    def __sub__(self, __other: "Point"):
        return Point(*(self.coords - __other.coords))
    
    def __hash__(self) -> int:
        a = 1
        s = 0
        for i in range(self.coords.shape[0]):
            s += a * self.coords[i]
            a *= self.n
            
        return int(s)
        
    def __eq__(self, value: "Point") -> bool:
        return np.all(self.coords == value.coords)
    
    def __gt__(self, __other: "Point") -> bool:
        eq = np.where(self.coords != __other.coords)[0]
        if eq.__len__() == 0:
            return False
        key_index = np.max(eq)
        return self.coords[key_index] > __other.coords[key_index]
    
    def __ge__(self, __other: "Point") -> bool:
        eq = np.where(self.coords != __other.coords)[0]
        if eq.__len__() == 0:
            return True
        key_index = np.max(eq)
        return self.coords[key_index] > __other.coords[key_index]
    
    def max_cord(self) -> int:
        return np.max(self.coords)
    
    def min_cord(self) -> int:
        return np.min(self.coords)
    
    def onTheSameLineFast(self, point2: "Point", point3: "Point"):
        v1 = (point2 - self).coords
        v2 = (point3 - self).coords
        angle = (v1 @ v2.transpose()) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        return np.arccos(np.clip(np.abs(angle), -1, 1)) < 1e-10
    
    def onTheSameLine(self, point2: "Point", point3: "Point"):
        for dim in range(self.coords.__len__() - 1):
            slope = None
            
            dx = point2.coords[dim] - self.coords[dim]
            if dx == 0:
                current_slope = float('inf')
            else:
                current_slope = (point2.coords[dim + 1] - self.coords[dim + 1]) / dx
            if slope is not None and current_slope != slope:
                return False
            
            slope = current_slope
            
            dx = point3.coords[dim] - point2.coords[dim]
            if dx == 0:
                current_slope = float('inf')
            else:
                current_slope = (point3.coords[dim + 1] - point2.coords[dim + 1]) / dx
            if slope is not None and current_slope != slope:
                return False
            
        return True
        
    