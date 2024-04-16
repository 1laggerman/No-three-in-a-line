
from matplotlib import pyplot as plt 
import numpy as np 
import matplotlib.animation as animation  

from package import GridPoints
import random
   
n = 5
d = 2
k = 2
   
ticks = np.arange(0, n, 1)
fig = plt.figure(figsize=(12, 10), dpi=80)
ax = plt.axes()  
ax.set_xticks(ticks)
ax.set_yticks(ticks)

gp = GridPoints(n=n, d=d, k_in_line=k)
   
for x in range(n):
    ax.plot([x, x], [0, n - 1], 'grey')
for y in range(n):
    ax.plot([0, n - 1], [y, y], 'grey')
# def __init__():
   
def animate(i): 
    # points = plt.scatter(gp.chosen) 
    if(len(gp.valid) != 0):
        added_point = random.choice(gp.valid)
        gp.add(added_point)
        ax.scatter([added_point.coords[0]], [added_point.coords[1]], s=500, c='r', edgecolor='black', linewidth=2)

    # for point in gp.chosen:
    #     ax.scatter([point.coords[0]], [point.coords[1]], s=500, c='r', edgecolor='black', linewidth=2)
    
    return ax,
   
anim = animation.FuncAnimation(fig, animate, frames = 100, interval = 500, blit = True) 

# plt.show()
writervideo = animation.PillowWriter(fps=60) 
anim.save('test.gif', writer=writervideo) 
plt.close() 