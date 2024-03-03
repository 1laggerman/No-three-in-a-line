
from .PointG import PointG as Point
from .GridG import GridG as Grid
from typing import Callable
import matplotlib.pyplot as plt
import math


def graph_avg(func: Callable[..., tuple[list[Point, int]]], *args, iters: int = 10, ns = range(3, 10), ds=range(2, 3)):
        results = []
        base = []
        for d in ds:
            for n in ns:
                g = Grid(n, d)
                sum = 0
                for _ in range(iters):
                    points, s = func(g, *args)
                    sum += s
                results.append(sum / iters)
                base.append(math.pow(n, d))
                print(f"finished n={n}, d={d}: {sum}")
            
        print("results\n", results)
        print("num of points: \n", base)
        plt.plot(results, base)
        plt.show()
        
def graph_cmpr(func: Callable[..., tuple[list[Point, int]]], *args, iters: int = 10, rg = range(3, 10), base: int = 3):
    results_n = []
    base_n = []
    
    for n in rg:
        g = Grid(n, base)
        sum = 0
        for _ in range(iters):
            points, s = func(g, *args)
            sum += s
        results_n.append(sum / iters)
        base_n.append(math.pow(n, base))
    
    plt.plot(results_n, base_n, color='blue', label='n')
    
    results_d = []
    base_d = []
    for d in rg:
        g = Grid(base, d)
        sum = 0
        for _ in range(iters):
            points, s = func(g, *args)
            sum += s
        results_d.append(sum / iters)
        base_d.append(math.pow(base, d))
        
    plt.plot(results_d, base_d, color='red', label='d')
    plt.show()