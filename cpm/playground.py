from data import Data
from lab_cpm import CriticalPath


task_data = Data("data.txt")
dto = CriticalPath.critical_path(task_data)

print(dto)
