from data import Data
from lab_cpm import find_critical_path_fixed


task_data = Data("data.txt")
# Find the corrected critical path for the graph
print(task_data)
critical_path_fixed, path_length_fixed = find_critical_path_fixed(task_data.full_graph)

print(critical_path_fixed, path_length_fixed)
