
from .Point import Point as Point
from .Grid import Grid as Grid
from typing import Callable
import matplotlib.pyplot as plt
import math
import json
from typing import TypedDict, List

class RunData(TypedDict):
    n: int
    d: int
    k: int
    avg_points: float
    total_runs: int
    
def precentile(data: RunData):
    max_points = data["k"] * math.pow(data["n"], data["d"] - 1)
    return data["avg_points"] / max_points

def graph(data_file: str, runner: str, base: tuple = (3, 2, 2), stop_at: int = 10, func: Callable[[RunData], float] = precentile):
    try:
        with open(data_file, "r") as json_file:
            existing_data: List[RunData] = json.load(json_file)
    except:
        return
    others = []
    values = ()
    if runner == "n":
        others = ["d", "k"]
        values = (base[1], base[2])
    elif runner == "d":
        others = ["n", "k"]
        values = (base[0], base[2])
    elif runner == "k":
        others = ["n", "d"]
        values = (base[0], base[1])
    else:
        return
    
    data = []
    axis = []
    for item in existing_data:
        if item[others[0]] == values[0] and item[others[1]] == values[1] and item[runner] < stop_at:
            data.append(func(item))
            axis.append(item[runner])
            
    print(data)
    print(axis)
    plt.plot(axis, data)
    plt.xlabel(runner)
    plt.ylabel(func.__name__)
    plt.show()
    

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
                print(f"finished n={n}, d={d}: {sum / iters}")
            
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
    

def run(func: Callable[..., tuple[list[Point, int]]], *args, iters: int = 5, ns = range(3, 10), ds=range(2, 3)):
    data: List[RunData] = []
    for d in ds:
        for n in ns:
            g = Grid(n, d)
            sum = 0
            for _ in range(iters):
                points, s = func(g, *args)
                sum += s
            res: RunData = {"n": n, "d": d, "k": 2, "avg_points": sum / iters, "total_runs": iters}
            data.append(res)
            print(f"finished n={n}, d={d}, k={2}: {sum / iters}")
    return data

def run_and_save(file_path: str, func: Callable[..., tuple[list[Point, int]]], *args, iters: int = 5, ns = range(3, 10), ds=range(2, 3)):
    data = run(func, *args, iters=iters, ns=ns, ds=ds)
    to_json_file(file_path, data, func.__name__)

def to_json_file(file_path: str, new_data: list[RunData], alg: str):
    filename = file_path + "/" + alg + ".JSON"

    try:
        with open(filename, "r") as json_file:
            existing_data: List[RunData] = json.load(json_file)
    except:
        existing_data = []
    # with open(filename, "r") as json_file:
    #     existing_data: List[RunData] = json.load(json_file)

    # Check if data for the given n, d, and k already exists
    add_to_data = []
    for new_item in new_data:
        found = False
        for item in existing_data:
            if item["n"] == new_item["n"] and item["d"] == new_item["d"] and item["k"] == new_item["k"]:
                item["avg_points"] = (item["avg_points"] * item["total_runs"] + new_item["avg_points"] * new_item["total_runs"]) / (item["total_runs"] + new_item["total_runs"])
                item["total_runs"] += new_item["total_runs"]
                found = True
                break
        if not found:
            add_to_data.append(new_item)

    existing_data.extend(add_to_data)
    # Write the updated data back to the file
    with open(filename, "w") as json_file:
        json.dump(existing_data, json_file)