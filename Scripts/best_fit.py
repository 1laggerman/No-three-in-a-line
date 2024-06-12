import sys
sys.path.insert(0, '') # this is so that python will know where to search for package
import numpy as np
import json
import matplotlib.pyplot as plt
from package.statistics import RunData

def get_poly(coeff):
    poly = ""
    power = len(coeff) - 1
    for i in range(len(coeff)):
        poly += "{:.2f}".format(coeff[i])
        if power > 0:
            poly += "x^({power})".format(power=power)
        # poly += "{:.2f}x^({power})".format(coeff[i], power=power)
        if i!= len(coeff) - 1:
            poly += " + "
            power -= 1
    return poly

with open('Data/min_conflict.JSON', "r") as json_file:
    existing_data: list[RunData] = json.load(json_file)
    
d = 6
k = 2
    
filter = [run for run in existing_data if run["d"] == d and run["k"] == k and run["args"]["max_iter"] == 1000]

filter.sort(key=lambda r: r["n"])
ns = [r["n"] for r in filter]
y1 = [r["avg_points"] for r in filter]
y2 = [r["max_points"] for r in filter]
i = [r["total_runs"] for r in filter]

c1 = np.polyfit(ns, y1, d - 1)
c2 = np.polyfit(ns, y2, d - 1)

print(c1)
print(c2)

# filter = [run for run in existing_data if run["d"] == d and run["k"] == k and run["args"]["max_iter"] == 1000]

# filter.sort(key=lambda r: r["n"])
# ns = [r["n"] for r in filter]
# y1 = [r["avg_points"] for r in filter]
# y2 = [r["max_points"] for r in filter]
# i = [r["total_runs"] for r in filter]




fig = plt.figure(figsize=(15, 10))

plt.scatter(ns, y1, c='r')
plt.scatter(ns, y2, c='b')
plt.plot(ns, np.polyval(c1, ns), c='r')
plt.plot(ns, np.polyval(c2, ns), c='b')
plt.title(f"best fit graph for min conflict d={d}, k={k}")
plt.xlabel("n")
plt.ylabel("points")
plt.legend([f"avg. plot: {get_poly(c1)}", f"max. plot: {get_poly(c2)}"])
plt.savefig(f"visuals/graphs/best_fit_d={d}, k={k}.png")
plt.show()