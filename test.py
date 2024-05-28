# import math
import numpy as np
# import matplotlib.pyplot as plt
from package.Point import Point as Point
from package.Grid import Grid as Grid
import json
from package.statistics import to_json_file, run_and_save, graph, run, RunData, counter
from package.GridPointsStruct import GridPoints
from package.collision import collision
import random

import itertools as it
from copy import deepcopy
import time
import math
import tqdm

# counter(math.pow(10, 8))
# iters = 10000
# i = 0
# for _ in tqdm.tqdm(range(iters)):
#     j = 0
#     with tqdm.tqdm(total=100000000, position=1, leave=False) as bar:
#         while j < 100000000:
#             j += 1
#             bar.update(1)
#     i += 1

# print(run(Grid.min_conflict, iters=10, ns=range(3, 11), ds=range(2, 5), ks=range(2, 5)))

run_and_save("Data", Grid.random_greedy, iters=10, ns=range(3, 11), ds=range(2, 5), ks=range(2, 5))

run_and_save("Data", Grid.min_conflict, iters=10, ns=range(3, 11), ds=range(2, 5), ks=range(2, 5))