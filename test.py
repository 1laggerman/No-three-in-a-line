# import math
import numpy as np
# import matplotlib.pyplot as plt
from package.Point import Point as Point
from package.Grid import Grid as Grid
import json
from package.statistics import to_json_file, run_and_save, graph, run, RunData, run_parallel, bind_func_args
from package.GridPointsStruct import GridPoints
from package.collision import collision
import random

import itertools as it
from copy import deepcopy
import time
import math
import tqdm



import multiprocessing
from multiprocessing import Pool, Manager


def counter(n: int):
    i = 0
    while i < n:
        i += 1
    print("Done!")
    

# def worker(args):
#     n, d, k, iters, func, func_args = args
#     g = Grid(n, d)
#     print(f'starting run for n={n}, d={d}, k={k}')

#     sum_points = 0
#     max_points = 0
#     for _ in range(iters):
#         func(*func_args)

#     return {"n": n, "d": d, "k": k, "avg_points": sum_points / iters, "max_points": max_points, "total_runs": iters, "args": func_args}

# def run_parallel_computation(ks, ds, ns, iters, func, func_args):
#     num_processes = multiprocessing.cpu_count()  # Automatically determine the number of processes to use
#     pool = Pool(processes=num_processes)
#     manager = Manager()
#     queue = manager.Queue()

#     results = []

#     tasks = [(n, d, k, iters, func, func_args) for k in ks for d in ds for n in ns]
#     async_results = [pool.apply_async(worker, (task,), callback=lambda x: queue.put(x)) for task in tasks]

#     pool.close()
#     pool.join()

#     # Collect all results from the queue
#     while not queue.empty():
#         result = queue.get()
#         results.append(result)
#         print(f"finished n={result['n']}, d={result['d']}, k={result['k']}")

#     return results

# Example usage
if __name__ == "__main__":
    ks = [2, 3, 4]
    ds = [2, 3, 4]
    ns = range(3, 11)
    iters = 5
    func = Grid.min_conflict  # Replace 'some_function' with the actual function you intend to use
    # func_args = ()  # Replace these with actual arguments for 'func'


    # bind_func_args(func, priority=[{'sorted': False, 'max_iter': 50}, {'max_iter': 150, 'abc': 5, 'a': 5}], max_iter=100, allowed_in_line=5)
    # results = run_parallel(func=func, ks=ks, ds=ds, ns=ns, iters=iters)
    run_and_save(file_path='Data', func=func, ks=ks, ds=ds, ns=ns, iters=iters, parallel=True, max_iter=100)
    # print(results)





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

# print(run_parallel(counter, iters=10, ns=range(3, 11), ds=[3], ks=[2]))

# run_and_save("Data", Grid.random_greedy, iters=10, ns=range(3, 11), ds=range(2, 5), ks=range(2, 5))

# run_and_save("Data", Grid.min_conflict, iters=5, ns=range(3, 11), ds=range(2, 5), ks=range(2, 5))