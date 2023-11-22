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
            
    def is_solution(self, points: list):
        points.extend(self.points)
        
        for point1, point2, point3 in it.combinations(points, 3):
            if point1.onTheSameLine(point2, point3):
                return False
        return True
            
    def removeInValidPoints(self, added1: Point, added2: Point, valid: list, d: Dimentions = Dimentions.D2, chosen: list = list()):
        valid.remove(added1)
        valid.remove(added2)
        
        if added1.x == added2.x:
            for i in range(self.n):
                if i != added1.y and i != added2.y:
                    try:
                        valid.remove(Point(added1.x, i))
                    except:
                        pass
                    
         
        for point1 in chosen:
            if point1 != added1 and point1 != added2:
                i = 0
                while i < len(valid):
                    if added1.onTheSameLine(point1, valid[i]) or added2.onTheSameLine(point1, valid[i]):
                        valid.remove(valid[i])
                        i = i - 1
                    i = i + 1
        return valid
                
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
                                ValidPoints.append(thisPoint)
                                
        return ValidPoints
    
    def smart_brute_recursive_2D(self):
        valid = self.getAllValidPoints()
        max_solutions = (list([self.points]), len(self.points))
        if len(self.points) == 0:
            max_solutions = self.choose_2_Xpoints_recursive_from_valid(2 * self.n, 0, valid)
        else:
            print("ERROR!")
        self.solutions = max_solutions[0]
        
        return len(self.solutions)
    
    def brute_force_recursive_2D(self):
        valid = self.getAllValidPoints()
        current_max = (list([self.points]), len(self.points))
        if len(self.points) == 0:
            for point1, point2 in it.combinations(valid, 2): # no point in choosing one and checking what is valid, everything is. this loop checks combinations of 2 points
                t = self.choose_points_recursive(2 * self.n, list((point1, point2)))
                if t[1] > current_max[1]:
                    current_max = t
                elif t[1] == current_max[1] or t[1] == 2 * self.n: # found another solution(at least one) with the same max
                    self.union_solutions(current_max[0], t[0], current_max[1])
                
        else:
            t = self.choose_points_recursive(2 * self.n)
        self.solutions = current_max[0]
        return (len(self.solutions), current_max[1])
    
    def union_solutions(self, set1: list, set2: list, length: int):
        for solution1 in set1:
            for solution2 in set2:
                i = 0
                while i < length and solution1[i] == solution2[i]:
                    i = i + 1
                if i == length:
                    set2.remove(solution2)
            
        # add all valid solutions:
        set1.extend(set2)
            
    def choose_points_recursive(self, max, chosen_points: list = list()):
        current_max = (list([list.copy(chosen_points)]), len(chosen_points) + len(self.points))
        if current_max[1] == max:
            return current_max
        validPoints = self.getAllValidPoints(chosen=list.copy(chosen_points))
        if len(validPoints) == 0:
            return current_max
        
        for point in validPoints:
            # find sorted location by of 3-dimentional point:
            loc = 0
            while loc < len(chosen_points) and point.x > chosen_points[loc].x:
                loc = loc + 1
            while loc < len(chosen_points) and point.x == chosen_points[loc].x and point.y > chosen_points[loc].y:
                loc = loc + 1
            while loc < len(chosen_points) and point.x == chosen_points[loc].x and point.y == chosen_points[loc].y and point.z > chosen_points[loc].z:
                loc = loc + 1
            if loc == len(chosen_points):
                chosen_points.append(point)
            else:
                chosen_points.insert(loc, point)
            
            # call recursively to choose other points and get the max result:
            t = self.choose_points_recursive(max, chosen_points=chosen_points)
            if t[1] > current_max[1]: # bigger max found, replace the old max
                current_max = t
            elif t[1] == current_max[1] or t[1] == max: # found another solution(at least one) with the same max
                self.union_solutions(current_max[0], t[0], current_max[1])
            chosen_points.remove(point)
        
        return current_max
    
    def choose_2_Xpoints_recursive_from_valid(self, max: int, x: int, validPoints: list, chosen_points: list = list()):
        current_max = (list([list.copy(chosen_points)]), len(chosen_points) + len(self.points))
        if current_max[1] == max:
            return current_max
        elif len(validPoints) < 2:
            if len(validPoints) == 1:
                current_max[0][0].append(validPoints[0])
            return current_max
        
        for i in range(len(validPoints)):
            if validPoints[i].x != x:
                break
            chosen_points.append(validPoints[i])
            
            j = i + 1
            while j < len(validPoints):
                if validPoints[j].x != x:
                    break
                chosen_points.append(validPoints[j])
                # call recursively to choose other points and get the max result:
                new_valid = self.removeInValidPoints(validPoints[i], validPoints[j], validPoints.copy(), Dimentions.D2, chosen_points)
                t = self.choose_2_Xpoints_recursive_from_valid(max, x + 1, new_valid, chosen_points=chosen_points)
                if t[1] > current_max[1]: # bigger max found, replace the old max
                    current_max = t
                elif t[1] == current_max[1] or t[1] == max: # found another solution(at least one) with the same max
                    self.union_solutions(current_max[0], t[0], current_max[1])
                chosen_points.pop()
                j = j + 1
            chosen_points.pop()
        
        return current_max
        
    def draw_grid(self, solutionID: int = -1, axis: str ='off'):
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
            if solutionID != -1:
                for point in self.solutions[solutionID]:
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
            
            for point in self.points: # paint all dots on grid
                ax.scatter([point.x], [point.y], [point.z], color='black', s=250)
            if solutionID != -1:
                for point in self.solutions[solutionID]:
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
            

n = 6
grid = Grid(n=n, d=2)
# grid.add_point(Point(0, 0))
# grid.add_point(Point(1, 1))

# valid1 = grid.getAllValidPoints(d=Dimentions.D2)

# chosen = list([valid1[0], valid1[1]])

# print("valid before: ")
# for point in valid1:
#     print(point)
# print(f"number of valid points: {len(valid1)}\ntotal number of points: {pow(grid.n, grid.d)}")

# valid1 = grid.removeInValidPoints(chosen[0], chosen[1], valid1, d=Dimentions.D2, chosen=chosen)
# chosen.append(valid1[0])
# chosen.append(valid1[1])
# print(f'------\n{valid1[0]}, {valid1[1]}\n-------')
# valid1 = grid.removeInValidPoints(valid1[0], valid1[1], valid1, d=Dimentions.D2, chosen=chosen)
# print("valid after: ")
# for point in valid1:
#     print(point)
# print(f"number of valid points: {len(valid1)}\ntotal number of points: {pow(grid.n, grid.d)}")



# valid = grid.getAllValidPoints(chosen=list([Point(1, 0, n=n)]))
# print("points on grid: ")
# for point in grid.points:
#     print(point)
# print("valid points:")
# for point in valid:
#     print(point)
# print(f"number of valid points: {len(valid)}\ntotal number of points: {pow(grid.n, grid.d)}")


max = grid.smart_brute_recursive_2D()
print('-------END RUN-------')
print(f"brute force max solution for n = {grid.n}: {max}")
i = 1
for s in grid.solutions:
    print(f'solution {i}')
    for point in s:
        print(point)
    i = i + 1

grid.draw_grid(0)

