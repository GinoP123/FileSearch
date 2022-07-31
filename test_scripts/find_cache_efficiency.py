#!/usr/bin/env python3

import os
import sys
fs_dir = os.getcwd().rstrip("/test_scripts/")
os.chdir(fs_dir)
sys.path.append(fs_dir)
import file_search
import settings

database = file_search.get_database()
len_sum = 0
cache_sum = 0

for row in database:
	len_sum += len(row[settings.PATH_IND])
	cache_sum += int(row[settings.SHIFT_IND])

print(f'\n\tcache: {cache_sum}, total: {len_sum}, {format(cache_sum / len_sum, ".1%")} Cached, {format(len_sum / (len_sum - cache_sum), ".1%")} Speedup\n')

