
from .Point import Point as Point
from .Grid import Grid as Grid
from .GridPointsStruct import GridPoints as GridPoints
from typing import Callable
import matplotlib.pyplot as plt
import math
import json
from typing import TypedDict, List
import inspect
import sys
import tqdm

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

class RunData(TypedDict):
    n: int
    d: int
    k: int
    avg_points: float
    max_points: int
    total_runs: int
    args: dict
    
def counter(n: int):
    i = 0
    try:
        while i < n:
            i += 1
    except KeyboardInterrupt:
        print('You pressed Ctrl+C!')
    
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
    fig = plt.figure(data_file.split('/')[-1].split('.')[0] + f" {others[0]}={values[0]}, {others[1]}={values[1]}")
    ax = plt.gca()
    # ax.set_xlim([xmin, xmax])
    ax.spines['top'].set_visible(False)
    ax.set_ylim([0, 1.01])
    plt.title(f"{others[0]}={values[0]}, {others[1]}={values[1]}")
    plt.plot(axis, data)
    plt.xlabel(runner)
    plt.ylabel(func.__name__)
    plt.show()
    

def graph_avg(func: Callable[..., GridPoints], *args, iters: int = 10, ns = range(3, 10), ds=range(2, 3)):
        results = []
        base = []
        for d in ds:
            for n in ns:
                g = Grid(n, d)
                sum = 0
                for _ in range(iters):
                    gp = func(g, *args)
                    sum += len(gp.chosen)
                results.append(sum / iters)
                base.append(math.pow(n, d))
                print(f"finished n={n}, d={d}: {sum / iters}")
            
        print("results\n", results)
        print("num of points: \n", base)
        plt.plot(results, base)
        plt.show()
        
def graph_cmpr(func: Callable[..., GridPoints], *args, iters: int = 10, rg = range(3, 10), base: int = 3):
    results_n = []
    base_n = []
    
    for n in rg:
        g = Grid(n, base)
        sum = 0
        for _ in range(iters):
            gp = func(g, *args)
            sum += len(gp.chosen)
        results_n.append(sum / iters)
        base_n.append(math.pow(n, base))
    
    plt.plot(results_n, base_n, color='blue', label='n')
    
    results_d = []
    base_d = []
    for d in rg:
        g = Grid(base, d)
        sum = 0
        for _ in range(iters):
            gp = func(g, *args)
            sum += len(gp.chosen)
        results_d.append(sum / iters)
        base_d.append(math.pow(base, d))
        
    plt.plot(results_d, base_d, color='red', label='d')
    plt.show()
    

def run(func: Callable[..., GridPoints], *args, iters: int = 5, ns = range(3, 10), ds=[2], ks=[2], **kwargs) -> List[RunData]:
    data: List[RunData] = []
    params_to_ignore = {'self', 'allowed_in_line', 'sorted', 'start_from'}
    sig = inspect.signature(func)
    func_params = {}
    g = Grid(3, 2)
    try:
        bound_args = sig.bind(g, *args, **kwargs)
        bound_args.apply_defaults()
        func_params = {name: value for name, value in bound_args.arguments.items() if name not in params_to_ignore}
    except:
        print("failed to bind args, data will not record function arguments.")
        i = input("press enter to continue, d for details or e to exit")
        if i == 'd':
            print('function arguments should be passed in the following format: run(n=3, d=2, k=2)')
        elif i == 'e':
            return
        
    try:
        for k in ks:
            for d in ds:
                for n in ns:
                    g = Grid(n, d)
                    print('staring run for n=', n, 'd=', d, 'k=', k)
                    
                    sum = 0
                    max_points = 0
                    for _ in tqdm.tqdm(range(iters)):
                        gp = func(g, *args, allowed_in_line=k)
                        num_points = len(gp.chosen)
                        if num_points > max_points:
                            max_points = num_points
                        sum += num_points
                    # with tqdm.tqdm(total=iters) as pbar:
                    #     for _ in range(iters):
                    #         gp = func(g, *args, allowed_in_line=k)
                    #         num_points = len(gp.chosen)
                    #         if num_points > max_points:
                    #             max_points = num_points
                    #         sum += num_points
                    #         pbar.update(1)
                    # for _ in range(iters):
                    #     gp = func(g, *args, allowed_in_line=k)
                    #     num_points = len(gp.chosen)
                    #     if num_points > max_points:
                    #         max_points = num_points
                    #     sum += num_points
                    res: RunData = {"n": n, "d": d, "k": k, "avg_points": sum / iters, "max_points": max_points, "total_runs": iters, "args": func_params}
                    data.append(res)
                    print(f"finished n={n}, d={d}, k={k}")
    except KeyboardInterrupt:
        print("interrupted by user, returning partial data")
    return data

def run_and_save(file_path: str, func: Callable[..., GridPoints], *args, iters: int = 5, ns = range(3, 10), ds=[2], ks=[2]):
    data = run(func, *args, iters=iters, ns=ns, ds=ds, ks=ks)
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
            if item["n"] == new_item["n"] and item["d"] == new_item["d"] and item["k"] == new_item["k"] and item["args"] == new_item["args"]:
                item["avg_points"] = (item["avg_points"] * item["total_runs"] + new_item["avg_points"] * new_item["total_runs"]) / (item["total_runs"] + new_item["total_runs"])
                item["total_runs"] += new_item["total_runs"]
                if item["max_points"] < new_item["max_points"]:
                    item["max_points"] = new_item["max_points"]
                found = True
                break
        if not found:
            add_to_data.append(new_item)

    existing_data.extend(add_to_data)
    # Write the updated data back to the file
    with open(filename, "w") as json_file:
        json.dump(existing_data, json_file)