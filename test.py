import math
import numpy as np
import matplotlib.pyplot as plt
from package.GridG import GridG as Grid

# n = np.array([-4, 8, 12])
# print(math.gcd(*n))
solutions = []

for i in range(18):
    g = Grid(i + 2, 2)
    s = g.random_greedy()
    solutions.append(s[1])
    
# print(solutions)
plt.plot(solutions)
plt.axis([2, 6, 4, 36])
plt.show()
# print(s)