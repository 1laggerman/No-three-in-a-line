import numpy as np

class Point:
    cords = np.ndarray
    
    def __init__(self, *coordinates: int, n: int = 3):
        self.cords = np.array([x for x in coordinates])
        self.n = n # max value of coordinates, for hashing porposes
        
    def __str__(self) -> str:
        pointStr = '('
        i = 0
        while i < self.cords.__len__() - 1:
            pointStr += f'{self.cords[i]}, '
            i = i + 1
        pointStr += f'{self.cords[i]})'
        return pointStr
    
    def __repr__(self):
        return str(self)
        
    def __add__(self, __other: "Point"):
        return Point(*(self.cords + __other.cords))
    
    def mul(self, __other: "Point"):
        return Point(*(self.cords * __other.cords))
    
    def __matmul___(self, __other: "Point"):
        return self.cords @ __other.cords
        
    def __truediv__(self, scalar):
        return Point(*(self.cords / scalar))
    
    def __floordiv__(self, scalar):
        return Point(*(self.cords // scalar))
    
    def __sub__(self, __other: "Point"):
        return Point(*(self.cords - __other.cords))
    
    def __hash__(self) -> int:
        a = 1
        s = 0
        for i in range(self.cords.shape[0]):
            s += a * self.cords[i]
            a *= self.n
            
        return int(s)
        
    def __eq__(self, value: "Point") -> bool:
        return np.all(self.cords == value.cords)
    
    def __gt__(self, __other: "Point") -> bool:
        eq = np.where(self.cords != __other.cords)[0]
        if eq.__len__() == 0:
            return False
        key_index = np.max(eq)
        return self.cords[key_index] > __other.cords[key_index]
    
    def __ge__(self, __other: "Point") -> bool:
        eq = np.where(self.cords != __other.cords)[0]
        if eq.__len__() == 0:
            return True
        key_index = np.max(eq)
        return self.cords[key_index] > __other.cords[key_index]
    
    def max_cord(self) -> int:
        return np.max(self.cords)
    
    def min_cord(self) -> int:
        return np.min(self.cords)
    
    def onTheSameLineFast(self, point2: "Point", point3: "Point"):
        v1 = (point2 - self).cords
        v2 = (point3 - self).cords
        angle = (v1 @ v2.transpose()) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        return np.arccos(np.clip(np.abs(angle), -1, 1)) < 1e-10
    
    def onTheSameLine(self, point2: "Point", point3: "Point"):
        for dim in range(self.cords.__len__() - 1):
            slope = None
            
            dx = point2.cords[dim] - self.cords[dim]
            if dx == 0:
                current_slope = float('inf')
            else:
                current_slope = (point2.cords[dim + 1] - self.cords[dim + 1]) / dx
            if slope is not None and current_slope != slope:
                return False
            
            slope = current_slope
            
            dx = point3.cords[dim] - point2.cords[dim]
            if dx == 0:
                current_slope = float('inf')
            else:
                current_slope = (point3.cords[dim + 1] - point2.cords[dim + 1]) / dx
            if slope is not None and current_slope != slope:
                return False
            
        return True
        
    