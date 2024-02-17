import numpy as np

class Point:
    x = 0
    y = 0
    z = 0

    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"
    def __repr__(self):
        return str(self)
        
    def __add__(self, __other: "Point"):
        return Point(self.x + __other.x, self.y + __other.y, self.z + __other.z)
    
    def __eq__(self, __value: "Point") -> bool:
        if self.x == __value.x and self.y == __value.y and self.z == __value.z:
            return True
        return False
    
    def __gt__(self, __other: "Point") -> bool:
        if self.z != __other.z:
            return self.z > __other.z
        elif self.x != __other.x:
            return self.x > __other.x
        return self.y > __other.y
    
    def __ge__(self, __other: "Point") -> bool:
        if self.z != __other.z:
            return self.z > __other.z
        if self.x != __other.x:
            return self.x >= __other.x
        return self.y >= __other.y
    
    def __hash__(self) -> int:
        return self.x + (self.y * self.n) + (self.z * pow(self.n, 2))
    
    def onTheSameLine(self, point2: "Point", point3: "Point"):
                
        if self == point2 or self == point3 or point2 == point3:
            return True
        
        dx2 = self.x - point2.x
        dx3 = self.x - point3.x
        dy2 = self.y - point2.y
        dy3 = self.y - point3.y
        
        if dx2 == 0 and dx3 == 0:
            # dx1 = 0, dx2 = 0
            if dy2 == 0 and dy3 == 0:
                return True
            elif dy2 == 0 or dy3 == 0:
                return False
            Myz2 = (self.z - point2.z) / dy2
            Myz3 = (self.z - point3.z) / dy3
            if Myz2 != Myz3:
                return False
            return True
        elif dx2 == 0 or dx3 == 0:
            return False

        Mxy2 = dy2 / dx2
        Mxy3 = dy3 / dx3
        if Mxy2 != Mxy3:
            return False
        Mxz2 = (self.z - point2.z) / dx2
        Mxz3 = (self.z - point3.z) / dx3
        if Mxz2 != Mxz3:
            return False
        return True
    
class PointG:
    cords = np.zeros(3, dtype=int)
    def __init__(self, cordinents):
        self.cords = np.array([x for x in cordinents])
        
    def __str__(self) -> str:
        pointStr = '('
        i = 0
        while i < self.cords.__len__() - 1:
            pointStr += f'{self.cords[i]}, '
            i = i + 1
        pointStr += f'{self.cords[i]})'
    
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
    
    def __ge__(self, __other: "Point") -> bool:
        eq = np.where(self.cords != __other.cords)[0]
        if eq.__len__() == 0:
            return True
        key_index = np.max(eq)
        return self.cords[key_index] > __other.cords[key_index]
    
    def get_max(self) -> int:
        return np.max(self.cords)
    
    # def onTheSameLine(self, point2: "PointG", point3: "PointG"):
        
    