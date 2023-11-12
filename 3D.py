import matplotlib.pyplot as plt
import numpy as np

class Point:
    x = 0
    y = 0

    def __init__(self, x = 0, y = 0):
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        self.x = int(x)
        self.y = int(y)
        
    def __add__(self, __other: object):
        return Point(self.x + __other.x, self.y + __other.y)
    
    def __eq__(self, __value: object) -> bool:
        if self.x == __value.x and self.y == __value.y:
            return True
        return False
        pass
    
    def onTheSameLine(self, point2, point3):
        m1 = np.abs((self.y - point2.y) / (self.x - point2.x))
        m2 = np.abs((self.y - point3.y) / (self.x - point3.x))
        if m1 != m2:
            return False
        return True
    
    def getAllValidPoints(n, points):
        ValidPoints = list()
        for i in range(n):
            for j in range(n):
                thisPoint = Point(i, j)
                for point1 in points:
                    for point2 in points:
                        if thisPoint != point1 != point2 and not thisPoint.onTheSameLine(point1, point2):
                            ValidPoints.append(thisPoint)
        return ValidPoints
                            
    def evalByDotsInLines(self, n, points):
        validPoints = self.getAllValidPoints(n, points)
        lines = dict()
        for diff in range(n):
            
            dotsCounter = 0
            line = list()
            dist = 1
            # loop for dx
            while ((self.x + (dist * diff) < n and self.y + dist < n) or (self.x - (dist * diff) > n and self.y - dist > n)):
                Pplus = Point(self.x + (dist * diff), self.y + dist)
                Pminus = Point(self.x - (dist * diff), self.y - dist)
                if (Pplus in validPoints):
                    dotsCounter = dotsCounter + 1
                    line.append(Pplus)
                if (Pminus in validPoints):
                    dotsCounter = dotsCounter + 1
                    line.append(Pminus)
                dist = dist + 1
            lines['%d'.format(diff)] = (line, dotsCounter)
            
            dotsCounter = 0
            line = list()
            dist = 1
            # loop for dy
            while ((self.x + dist < n and self.y + (dist * diff) < n) or (self.x - dist > n and self.y - (dist * diff) > n)):
                Pplus = Point(self.x + dist, self.y + (dist * diff))
                Pminus = Point(self.x - dist, self.y - (dist * diff))
                if (Pplus in validPoints):
                    dotsCounter = dotsCounter + 1
                    line.append(Pplus)
                if (Pminus in validPoints):
                    dotsCounter = dotsCounter + 1
                    line.append(Pminus)
                dist  = dist + 1
            lines['%d'.format(diff)] = (line, dotsCounter)
            
class grid:
    points = []
    n = 1
    d = 2
    
    def __init__(self, n = 1, d = 2):
        if n < 1:
            n = 1
        if d < 2:
            d = 2
        self.n = int(n)
        self.d = int(d)
        
    def drawGrid(self, axis='off'):
        ticks = np.arange(0, n, 1)
        fig = plt.figure(figsize=(15, 15), dpi=80)
        if self.d == 2:
            ax = plt.axes()
        elif self.d == 3:
            ax = plt.axes(projection='3d')
            ax.set_zticks(ticks)
            ax.set_zlim(0, n - 1)
            
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        ax.set_xlim(0, n - 1)
        ax.set_ylim(0, n - 1)
        
        
        if self.d == 2:
            for x in range(n):
                for y in range(n):
                    if x == 0:
                        ax.plot([0, n - 1], [y, y], 'grey')
                    if y == 0:
                        ax.plot([x, x], [0, n - 1], 'grey')

            ax.scatter([0], [0], color='black', s=250) # scatter all dots instead
            
        elif self.d == 3:            
            for x in range(n):
                for y in range(n):
                    for z in range(n):
                        if x == 0:
                            ax.plot3D([0, n - 1], [y, y], [z, z], 'grey')
                        if y == 0:
                            ax.plot3D([x, x], [0, n - 1], [z, z], 'grey')
                        if z == 0:
                            ax.plot3D([x, x], [y, y], [0, n - 1], 'grey')

            ax.plot3D([0, n - 1], [0, 0], [0, 0], 'red') # red to visualize X axis
            ax.plot3D([0, 0], [0, n - 1], [0, 0], 'green') # green to visualize Y axis
            ax.plot3D([0, 0], [0, 0], [0, n - 1], 'blue') # blue to visualize Z axis
            
            ax.scatter([0], [0], [0], color='black', s=250) # scatter all dots instead
            
        else:
            print('figure cannot be shown for %d dimentions'.format(self.d))
            
        if axis == 'off':
            plt.axis('off')
        else:
            ax.set_xlabel('X axis')
            ax.set_ylabel('Y axis')
            ax.set_zlabel('Z axis')
        plt.show()
            

n = 5 # grid size

fig = plt.figure(figsize=(15, 15), dpi=80)
ticks = np.arange(0, n, 1)
ax = plt.axes(projection='3d')
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_zticks(ticks)

for x in range(n):
    for y in range(n):
        for z in range(n):
            if x == 0:
                ax.plot3D([0, n - 1], [y, y], [z, z], 'grey')
            if y == 0:
                ax.plot3D([x, x], [0, n - 1], [z, z], 'grey')
            if z == 0:
                ax.plot3D([x, x], [y, y], [0, n - 1], 'grey')

ax.plot3D([0, n - 1], [0, 0], [0, 0], 'red') # red for X axis
ax.plot3D([0, 0], [0, n - 1], [0, 0], 'green') # green for Y axis
ax.plot3D([0, 0], [0, 0], [0, n - 1], 'blue') # blue for Z axis


ax.scatter([0], [0], [0], color='black', s=250) # scatter a single dot on (0, 0, 0)

ax.set_xlim(0, n - 1)
ax.set_ylim(0, n - 1)
ax.set_zlim(0, n - 1)

# view with axis:
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

# view as "naked" cube
# plt.axis('off') 

plt.show()