import numpy as np

class PointG:
    cords = np.zeros(3, dtype=int)
    
    def __init__(self, *cordinents):
        self.cords = np.array([x for x in cordinents])
        
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
        
    def __add__(self, __other: "PointG"):
        return PointG(self.cords + __other.cords)
    
    def mul(self, __other: "PointG"):
        return PointG(self.cords * __other.cords)
    
    def __matmul___(self, __other: "PointG"):
        return self.cords @ __other.cords
        
    def __truediv__(self, scalar):
        return PointG(self.cords / scalar)
    
    def __sub__(self, __other: "PointG"):
        return PointG(self.cords - __other.cords)
    
    def __eq__(self, __value: "PointG") -> bool:
        return np.all(self.cords == __value.cords)
    
    def __gt__(self, __other: "PointG") -> bool:
        eq = np.where(self.cords != __other.cords)[0]
        if eq.__len__() == 0:
            return False
        key_index = np.max(eq)
        return self.cords[key_index] > __other.cords[key_index]
    
    def __ge__(self, __other: "PointG") -> bool:
        eq = np.where(self.cords != __other.cords)[0]
        if eq.__len__() == 0:
            return True
        key_index = np.max(eq)
        return self.cords[key_index] > __other.cords[key_index]
    
    def get_max(self) -> int:
        return np.max(self.cords)
    
    def onTheSameLineFast(self, point2: "PointG", point3: "PointG"):
        v1 = point2.cords - self.cords
        v2 = point3.cords - self.cords
        angle = (v1 @ v2.transpose()) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        return np.arccos(np.clip(np.abs(angle), -1, 1)) < 1e-10
    
    def onTheSameLine(self, point2: "PointG", point3: "PointG"):
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
        
    