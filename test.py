import math
import numpy as np
from package.GridG import GridG as Grid

n = np.array([-4, 8, 12])
print(math.gcd(*n))

g = Grid(3, 2)
solution = g.random_greedy()
print(solution)