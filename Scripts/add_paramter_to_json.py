
import sys
sys.path.insert(0, '') # this is so that python will know where to search for package

from package.statistics import RunData
import json
import math

# script for adding additional value to RunData 

filename = "Data/min_conflict.JSON"

with open(filename, "r") as json_file:
    existing_data: list[RunData] = json.load(json_file)

for item in existing_data:
    item["args"]['start_from'] = None
    
updated_data = existing_data
print(existing_data)
    


# reorder items loop
# desired_order = ['n', 'd', 'k', 'avg_points', 'max_points', 'total_runs', 'args']

# updated_data = []
# for item in existing_data:
#     # Calculate max_points and insert it into the dictionary
#     item["max_points"] = math.ceil(item["avg_points"])
    
#     # Rebuild the dictionary in the specified order
#     reordered_item = {key: item[key] for key in desired_order if key in item}
#     updated_data.append(reordered_item)
#     print(reordered_item)

# for item in existing_data:
#     print(item)




# with open(filename, "w") as json_file:
#     json.dump(updated_data, json_file)
