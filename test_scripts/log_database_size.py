#!/usr/bin/env python3

import sys
import os
import datetime
fs_dir = f"{os.path.dirname(sys.argv[0])}/.."
os.chdir(fs_dir)
sys.path.append(fs_dir)
import settings

with open(settings.DB_FILE) as infile:
	size = len(infile.readlines())

date = datetime.date.today().strftime("%m/%d/%Y")
with open(settings.DB_SIZES, 'a') as outfile:
	outfile.write(f"{size} {date}\n")

