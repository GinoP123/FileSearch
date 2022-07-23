#!/usr/bin/env python3

import sys
import os
import library as lb


if __name__ == "__main__":
	args = sys.argv
	os.chdir(os.path.dirname(args[0]))
	
	assert len(args) >= 2
	if args[1] == 'add_path':
		assert len(args) == 3
		lb.add_path(args[2])
	elif args[1] == 'search':
		assert len(args) == 3
		keys = args[2].split()
		lb.search(keys)
	elif args[1] == 'get_output':
		lb.get_last_output()
	elif args[1] == 'delete':
		assert len(args) == 3
		db = lb.get_database()
		lb.remove_path(db, args[2])
	else:
		raise AssertionError("Invalid Option")

