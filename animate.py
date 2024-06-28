
# importing required libraries 
from matplotlib import pyplot as plt 
import numpy as np 
import matplotlib.animation as animation
import random
import os
ffmpeg_source = "C:/ProgramData/anaconda3/Library/bin/ffmpeg"
plt.rcParams['animation.ffmpeg_path'] = ffmpeg_source
# import ffmpeg

from package import GridPoints
from package.collision import collision
from package.Point import Point

import itertools as it
  
n = 5
d = 2
k = 2    

def choose(condition: np.ndarray):
    choose_from = np.where(condition)
    point_idx = np.random.choice(range(len(choose_from[0])))
    point_coords = tuple([choose_from[i][point_idx] for i in range(d)])
    point = Point(*point_coords, n=n)
    
    return point 

ticks = np.arange(0, n, 1)
fig = plt.figure(dpi=80) 
axis = plt.axes(xlim=(0, 5),  ylim=(0, 5)) 
x, y = [], [] 
  
  
line, = axis.plot(0, 0) 
  
gp = GridPoints(n, d, k)

vectorized_func = np.vectorize(collision.num)

gp.adding = True

def animate(frame_number):
    if frame_number > 0 and frame_number % 2 == 0: 
        if len(gp.valid) > 0:
            # print('adding point', len(gp.chosen), 'at frame ', frame_number)
            added_point = random.choice(gp.valid)
            gp.add(added_point)
        elif len(gp.chosen) < k * n or gp.adding == False:
            collision_count = vectorized_func(gp.collision_mat)
            if gp.adding:
                legal_collision = gp.idx_mat <= 0
                collisions = np.logical_and(collision_count >= 0, legal_collision)
                gp.min_conflict_value = np.min(np.where(collisions, collision_count, np.inf))
                min_conflict_points: np.ndarray = np.logical_and(collision_count == gp.min_conflict_value, legal_collision)
                
                added_point = choose(min_conflict_points)
                
                gp.add(added_point)
                gp.adding = False
            else:
                if len(gp.conflicted) != 0 and gp.min_conflict_value != 0:
                    c = random.choice(gp.conflicted)
                    gp.remove(c)
                gp.adding = True
    
    axis.clear()
    axis.set_xticks(ticks)
    axis.set_yticks(ticks)
    for x in range(n):
        axis.plot([x, x], [0, n - 1], 'grey')
    for y in range(n):
        axis.plot([0, n - 1], [y, y], 'grey')
    for point in gp.chosen:
        axis.scatter([point.coords[0]], [point.coords[1]], s=500, c='r', edgecolor='black', linewidth=2)
    for point in gp.valid:
        axis.scatter([point.coords[0]], [point.coords[1]], s=250, c='b', edgecolor='black', linewidth=2)
        
    for p in it.product(range(n), repeat=d):
        slot: collision = gp.collision_mat[p]
        axis.scatter([p[0]], [p[1]], s=100 * slot.amount, c='g', edgecolor='black', linewidth=2)
    # for point in gp.conflicted:
    #     # slot: collision = gp.collision_mat[tuple(point.coords)]
    #     axis.scatter([point.coords[0]], [point.coords[1]], s=500, c='purple', edgecolor='black', linewidth=2)
    plt.axis('off')
    return line, 
  
  
anim = animation.FuncAnimation(fig, animate, frames=50, interval=50, blit=True) 
# fig.suptitle('Straight Line plot', fontsize=14) 
  
# plt.show()
  
# saving to m4 using ffmpeg writer 
# writervideo = animation.FFMpegWriter(fps=1)
writervideo = animation.PillowWriter(fps=1)
anim.save('min_conflict_2.gif', writer=writervideo) 
plt.close() 