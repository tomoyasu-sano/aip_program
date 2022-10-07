"""
台の連番を作る

"""

import pandas as pd

start = 1337
end = 1360

table_list = []
for no in range(start, end+1):
    table_list.append(no)


print(f"start table: {start}")
print(f"table length: {len(table_list)}")
print(table_list)
