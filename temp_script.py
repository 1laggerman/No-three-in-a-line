from package.statistics import RunData
import json

# script for adding additional value to RunData 

filename = "Data/random_greedy.JSON"

with open(filename, "r") as json_file:
    existing_data: list[RunData] = json.load(json_file)

for item in existing_data:
    item["max_points"] = int(item["avg_points"]) + 1
    item["args"] = {}
    print(item)
    print(item["avg_points"])




# with open(filename, "w") as json_file:
#     json.dump(existing_data, json_file)
