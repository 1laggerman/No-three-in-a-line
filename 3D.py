import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
import itertools as it

class Dimentions(Enum):
    D2 = 2
    D3 = 3
    

class Point:
    x = 0
    y = 0
    z = 0

    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if z < 0:
            z = 0
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"
        
    def __add__(self, __other: "Point"):
        return Point(self.x + __other.x, self.y + __other.y, self.z + __other.z)
    
    def __eq__(self, __value: "Point") -> bool:
        if self.x == __value.x and self.y == __value.y and self.z == __value.z:
            return True
        return False
    
    def onTheSameLine(self, point2: "Point", point3: "Point"):
        # fix dx = 0 problem
        
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
            
class Grid:
    points = list()
    n = 1
    d = 2
    
    def __init__(self, n: int = 1, d: int = 2):
        if n < 1:
            n = 1
        if d < 2:
            d = 2
        self.n = n
        self.d = d
        
    def add_point(self, p: Point):
        self.points.append(p)
        
    def add_points(self, points_arr: list):
        for point in points_arr:
            self.points.append(point)
        
    def getAllValidPoints(self, d: Dimentions = Dimentions.D2, z_layer: int = 0, chosen: list = list()):
        chosen.extend(self.points)
        ValidPoints = list()
        for x in range(self.n):
            for y in range(self.n):
                if d == Dimentions.D2:
                    if len(self.points) > 0:
                        z = chosen[0].z
                    else:
                        z = z_layer
                    thisPoint = Point(x, y, z)
                    
                    if len(chosen) == 0:
                        ValidPoints.append(thisPoint)
                    elif len(chosen) == 1:
                        if thisPoint != chosen[0]:
                            ValidPoints.append(thisPoint)
                    else:
                        pointValid = True
                        for point1, point2 in it.combinations(chosen, 2):
                            if thisPoint.onTheSameLine(point1, point2):
                                pointValid = False
                        if pointValid:
                            ValidPoints.append(thisPoint)
                elif d == Dimentions.D3:
                    for z in range(self.n):
                        thisPoint = Point(x, y, z)
                        
                        if len(self.points) == 0:
                            ValidPoints.append(thisPoint)
                        elif len(self.points) == 1:
                            if thisPoint != chosen[0]:
                                ValidPoints.append(thisPoint)
                        else:
                            pointValid = True
                            for point1, point2 in it.combinations(self.points, 2):
                                if thisPoint.onTheSameLine(point1, point2):
                                    pointValid = False
                            if pointValid:
                                # print(f"this: {thisPoint}, 1: {point1}")
                                ValidPoints.append(thisPoint)
                                
                                    
        return ValidPoints
    
    def brute_force_recursive_2D(self):
        valid = self.getAllValidPoints()
        max = (self.points, len(self.points))
        if len(self.points) == 0:
            for point1, point2 in it.combinations(valid, 2): # no point in choosing one and checking what is valid, everything is. this loop checks combinations of 2 points
                t = self.choose_points_recursive(2 * self.n, list((point1, point2)))
                # for point in t[0]:
                    # print(point)
                if t[1] > max[1]:
                    max = t
                # print("------")
                
        else:
            max = self.choose_points_recursive(2 * self.n)
        self.add_points(max[0])
        return max[1]
            
            
    def choose_points_recursive(self, max, chosen_points: list = list()):
        current_max = (chosen_points, len(chosen_points) + len(self.points))
        if current_max[1] == max:
            return current_max
        validPoints = self.getAllValidPoints(chosen_points)
        if len(validPoints) == 0:
            return current_max
        
        print("looking...")
        
        for point in validPoints:
            chosen_points.append(point)
            t = self.choose_points_recursive(max, chosen_points)
            # print(type(t))
            if t[1] > current_max[1]:
                current_max = t
                if current_max[1] == max:
                    return current_max
            chosen_points.remove(point)
        
        return current_max
            
            
        # for point1, point2 in it.combinations(self.points, 2):
        
    def draw_grid(self, axis: str ='off'):
        ticks = np.arange(0, self.n, 1)
        fig = plt.figure(figsize=(12, 10), dpi=80)
        if self.d == 2:
            ax = plt.axes()
        elif self.d == 3:
            ax = plt.axes(projection='3d')
            ax.set_zticks(ticks)
            ax.set_zlim(0, self.n - 1)
            
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        # ax.set_xlim(-0.1, self.n - 0.9)
        # ax.set_ylim(-0.1, self.n - 0.9)
        
        
        if self.d == 2:
            for x in range(self.n):
                ax.plot([x, x], [0, self.n - 1], 'grey')
            for y in range(self.n):
                ax.plot([0, self.n - 1], [y, y], 'grey')

            for point in self.points:
                ax.scatter([point.x], [point.y], color='black', s=250)
            
        elif self.d == 3:
            # paint grid lines:
            
            # paint X-lines:
            for y in range(self.n):
                for z in range(self.n):
                    ax.plot3D([0, self.n - 1], [y, y], [z, z], 'grey')
            
            # paint Y-lines:
            for x in range(self.n):
                for z in range(self.n):
                    ax.plot3D([x, x], [0, self.n - 1], [z, z], 'grey')
            
            # paint Z-lines:
            for x in range(self.n):
                for y in range(self.n):
                    ax.plot3D([x, x], [y, y], [0, self.n - 1], 'grey')        

            # paint lines from (0, 0 ,0) to visualize directions:
            ax.plot3D([0, self.n - 1], [0, 0], [0, 0], 'red') # paint red to visualize X axis
            ax.plot3D([0, 0], [0, self.n - 1], [0, 0], 'green') # green to visualize Y axis
            ax.plot3D([0, 0], [0, 0], [0, self.n - 1], 'blue') # blue to visualize Z axis
            
            for point in self.points: # paint all dots
                ax.scatter([point.x], [point.y], [point.z], color='black', s=250)
            
        else:
            print('figure cannot be shown for %d dimentions'.format(self.d))
            
        if axis == 'off':
            plt.axis('off')
        else:
            ax.set_xlabel('X axis')
            ax.set_ylabel('Y axis')
            if self.d == 3:
                ax.set_zlabel('Z axis')
            
        # manager = plt.get_current_fig_manager()
        # manager.full_screen_toggle()
        # ax.margins(0.02)
        plt.show()
            

grid = Grid(3, 2)
grid.add_point(Point(0, 0))
grid.add_point(Point(0, 1))
valid = grid.getAllValidPoints()
for point in grid.points:
    print(point)
print('-----')
for point in valid:
    print(point)
print(f"number of valid points: {len(valid)}\ntotal number of points: {pow(grid.n, grid.d)}")

grid.draw_grid()

