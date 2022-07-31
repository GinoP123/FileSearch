#!/usr/bin/env python3

import sys
import os
import datetime
fs_dir = os.getcwd().rstrip("/test_scripts/")
os.chdir(fs_dir)
sys.path.append(fs_dir)
import settings

with open(settings.DB_FILE) as infile:
	size = len(infile.readlines())

date = datetime.date.today().strftime("%m/%d/%Y")
with open(, 'a') as outfile:
	outfile.write(f"{size} {date}\n")

