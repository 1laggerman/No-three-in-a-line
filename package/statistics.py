
from .Point import Point as Point
from .Grid import Grid as Grid
from .GridPointsStruct import GridPoints as GridPoints
from typing import Callable
import matplotlib.pyplot as plt
import math
import json
from typing import TypedDict, List, Any
import inspect
import sys
import tqdm
import multiprocessing
import logging
import time

class RunData(TypedDict):
    n: int
    d: int
    k: int
    avg_points: float
    max_points: int
    total_runs: int
    args: dict
    
    
dont_save_params = set([
    'self',
    'sorted',
    'show_progress',
    'allowed_in_line',    
])
    
def avg_precentile(data: RunData):
    max_points = data["k"] * math.pow(data["n"], data["d"] - 1)
    return data["avg_points"] / max_points

def avg_points(data: RunData):
    return data["avg_points"]

def max_precentile(data: RunData):
    max_points = data["k"] * math.pow(data["n"], data["d"] - 1)
    return data["max_points"] / max_points

def max_points(data: RunData):
    return data["max_points"]

def scatter(data: list[RunData], show: tuple[bool] = (True, True)):
    for elemnt in data:
        if show[0]:
            plt.scatter(elemnt["n"], elemnt["avg_points"], c='r')
        if show[1]:
            plt.scatter(elemnt["n"], elemnt["max_points"], c='b')
            
# def make_plot()

def plot_line(data_file: str, runner: str, base: tuple = (3, 2, 2), stop_at: int = 10, func: Callable[[RunData], float] = max_points):
    try:
        with open(data_file, "r") as json_file:
            existing_data: List[RunData] = json.load(json_file)
    except:
        return
    
    mapping = {
        "n": 0,
        "d": 1,
        "k": 2,
    }
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
        if item[others[0]] == values[0] and item[others[1]] == values[1] and item[runner] < stop_at and item[runner] >= base[mapping[runner]]:
            data.append((func(item), item[runner]))
            # data.append(func(item))
            
    data.sort(key=lambda x: x[1])
    axis = [x[1] for x in data]
    data = [x[0] for x in data]
    print(data)
    print(axis)
    fig = plt.figure(data_file.split('/')[-1].split('.')[0] + f" {others[0]}={values[0]}, {others[1]}={values[1]}")
    ax = plt.gca()
    # ax.set_xlim([xmin, xmax])
    ax.spines['top'].set_visible(False)
    # ax.set_ylim([0, 1.01])
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
    

def run_linear(func: Callable[..., GridPoints], *args, iters: int = 5, ns = range(3, 10), ds=[2], ks=[2], **kwargs) -> List[RunData]:
    data: List[RunData] = []
    func_args = bind_func_args(func, priority=[kwargs, {'sorted': False}], *args, **kwargs)
    try:
        del func_args['allowed_in_line']
    except:
        pass
    
    save_args = {name: value for name, value in func_args.items() if name not in dont_save_params}
        
    start_time = time.time()
    try:
        for k in ks:
            for d in ds:
                for n in ns:
                    g = Grid(n, d)
                    
                    sum = 0
                    max_points = 0
                    
                    for _ in tqdm.tqdm(range(iters), desc=f'{n}, {d}, {k}', leave=True):
                        gp = func(g, **func_args, allowed_in_line=k)
                        num_points = len(gp.chosen)
                        if num_points > max_points:
                            max_points = num_points
                        sum += num_points
                    res: RunData = {"n": n, "d": d, "k": k, "avg_points": sum / iters, "max_points": max_points, "total_runs": iters, "args": save_args}
                    data.append(res)
    except KeyboardInterrupt:
        print("interrupted by user, returning partial data: ")
        print(data)
    end_time = time.time()
    print("total time: ", end_time - start_time)
    return data

def batch_worker(args):
    i, n, d, k, iters, func, func_params, save_args = args
    g = Grid(n, d)

    sum_points = 0
    max_points = 0
    
    try:
        # with tqdm.tqdm(total=iters, position=i + 1, leave=True, desc=f'{n}, {d}, {k}') as bar:
            for j in range(iters):
                gp = func(g, **func_params, allowed_in_line=k)
                num_points = len(gp.chosen)
                if num_points > max_points:
                    max_points = num_points
                sum_points += num_points
                # bar.update(1)
    except KeyboardInterrupt:
        print("interrupted by user, returning partial data: ")
        iters = j
        pass
        
    return {"n": n, "d": d, "k": k, "avg_points": sum_points / iters, "max_points": max_points, "total_runs": iters, "args": save_args}

def worker(args):
    i, n, d, k, func, func_params = args
    g = Grid(n, d)
    
    try:
        gp: GridPoints = func(g, **func_params, allowed_in_line=k)
        num_points = len(gp.chosen)
    except KeyboardInterrupt:
        return (i, None)
        
    return (i, num_points)

def run_parallel(func: Callable[..., GridPoints], *args, iters: int = 5, ns = range(3, 10), ds=[2], ks=[2], **kwargs) -> List[RunData]:
    
    data: List[RunData] = []
    func_args = bind_func_args(func, priority=[{'show_progress': False}, kwargs, {'sorted': False}], *args, **kwargs)
    try:
        del func_args['allowed_in_line']
    except:
        pass

    save_args = {name: value for name, value in func_args.items() if name not in dont_save_params}
    
    jobs = [(n, d, k) for k in ks for d in ds for n in ns]
    
    jobs.sort(key=lambda j: math.pow(j[0], j[1]) / j[2], reverse=True) # sort so the heaviest tasks are first.
    
    jobs = [(i, (n, d, k)) for i, (n, d, k) in enumerate(jobs)]
    
    results = []
    for i, (n, d, k) in jobs:
        results.append({"n": n, "d": d, "k": k, "avg_points": 0, "max_points": 0, "total_runs": 0, "args": save_args})

    tasks = [(i, n, d, k, func, func_args) for i, (n, d, k) in jobs for _ in range(iters)]
    
    num_processes = min(multiprocessing.cpu_count(), len(tasks))
    print(f"running with {num_processes} processes")

    pool = multiprocessing.Pool(processes=num_processes)
    manager = multiprocessing.Manager()
    queue = manager.Queue()
    
    time_start = time.time()
    
    total_tasks = len(tasks)
    with tqdm.tqdm(total=total_tasks, position=0, leave=True) as pbar:
        for task in tasks:
            pool.apply_async(worker, (task,), callback=lambda x: (queue.put(x), pbar.update(1)))

        pool.close()
        pool.join()

    pool.close()
    pool.join()
    
    time_end = time.time()

    # Collect all results from the queue
    while not queue.empty():
        result = queue.get()
        data.append(result)
        
    for i, num in data:
        if num is not None:
            total = results[i]["total_runs"]
            results[i]["avg_points"] = (results[i]["avg_points"] * total + num) / (total + 1)
            results[i]["max_points"] = max(results[i]["max_points"], num)
            results[i]["total_runs"] += 1
            
    print("total time: ", time_end - time_start)
            
    return results
    

def run_batch_parallel(func: Callable[..., GridPoints], *args, iters: int = 5, ns = range(3, 10), ds=[2], ks=[2], **kwargs) -> List[RunData]:
    data: List[RunData] = []
    
    func_args = bind_func_args(func, priority=[{'show_progress': False}, kwargs, {'sorted': False}], *args, **kwargs)
    try:
        del func_args['allowed_in_line']
    except:
        pass
    
    save_args = {name: value for name, value in func_args.items() if name not in dont_save_params}
        
    num_processes = multiprocessing.cpu_count()

    pool = multiprocessing.Pool(processes=num_processes)
    manager = multiprocessing.Manager()
    queue = manager.Queue()
    
    time_start = time.time()
    
    jobs = [(n, d, k) for k in ks for d in ds for n in ns]
    jobs.sort(key=lambda j: math.pow(j[0], j[1]) / j[2], reverse=True) # sort so the heaviest tasks are first.

    tasks = [(i, n, d, k, iters, func, func_args, save_args) for i, (n, d, k) in enumerate(jobs)]
    
    total_tasks = len(tasks)
    with tqdm.tqdm(total=total_tasks, position=0, leave=True) as pbar:
        for task in tasks:
            pool.apply_async(batch_worker, (task,), callback=lambda x: (queue.put(x), pbar.update(1)))

        pool.close()
        pool.join()

    pool.close()
    pool.join()

    time_end = time.time()
    # Collect all results from the queue
    while not queue.empty():
        result = queue.get()
        data.append(result)
        
    print("total time: ", time_end - time_start)
    return data

def run_and_save(file_path: str, func: Callable[..., GridPoints], *args, iters: int = 5, ns = range(3, 10), ds=[2], ks=[2], parallel=False, **kwargs) -> None:
    data: list[RunData] = []
    if parallel:
        data = run_parallel(func, *args, iters=iters, ns=ns, ds=ds, ks=ks, **kwargs)
        # data = run_batch_parallel(func, *args, iters=iters, ns=ns, ds=ds, ks=ks, **kwargs)
    else:
        data = run_linear(func, *args, iters=iters, ns=ns, ds=ds, ks=ks, **kwargs)
    to_json_file(file_path, data, func.__name__)

def to_json_file(file_path: str, new_data: list[RunData], alg: str):
    filename = file_path + "/" + alg + ".JSON"

    try:
        with open(filename, "r") as json_file:
            existing_data: List[RunData] = json.load(json_file)
    except:
        existing_data = []

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
        
def bind_func_args(func: Callable[..., GridPoints], priority: list[dict[str, Any]], *args, **kwargs) -> dict[str, Any]:
    sig = inspect.signature(func)
    g = Grid(3, 2) # default object required for binding
    
    try:
        bound_args = sig.bind(g, *args, **kwargs) # bind function with default object
        bound_args.apply_defaults() # apply default arguments
        
        func_args = {name: value for name, value in bound_args.arguments.items()} # dict of all default default arguments
        
        for i in range(1, len(priority)):
            pos = len(priority) - i - 1
            filtered_dict = {k: priority[pos][k] for k in priority[pos] if k in func_args}
            func_args.update(filtered_dict)
        
        del func_args['self'] # remove self argument
        
    except:
        logging.exception('Error accured while binding function arguments')
        # print("")
        print('\nthis Exception accured because the function arguments were not passed in the correct format.')
        print('this is likely a cause of one of the following:\n')
        print('\t1. type error in the name of an argument')
        print('\t2. missmatching argument type. to avoid this use key=value syntax when passing arguments')
        print('\t3. argument with no default value had no value passed in\n')
        exit(1)
        
    return func_args