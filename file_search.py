#!/usr/bin/env python3

import heapq
import sys
import settings
import os
import csv
import bisect


def remove_chars(string):
	string = string.lower()
	new_str = ''
	for char in string:
		if char not in '_/ \n\t':
			new_str += char
	return new_str


def match_score(a, b):
	return 1 if a == b else -1


def get_database():
	with open(settings.DB_FILE) as db_file:
		return [row for row in csv.reader(db_file)]


def update_database(database):
	with open(settings.DB_FILE, 'w') as outfile:
		csv.writer(outfile).writerows(database)


def get_neighboring_paths(path):
	if os.path.exists(path):
		dirname = path if os.path.isdir(path) else os.path.dirname(path)
		siblings = [os.path.join(dirname, name) for name in os.listdir(dirname)]
		return [dirname] + siblings
	return [path]


def get_insert_index(database, path):
	index = bisect.bisect(database, [path, ""])
	if index >= len(database) or database[index][0] != path:
		return index
	return -1


def add_path(path):
	database = get_database()
	candidates = get_neighboring_paths(path)

	adds = []
	for candidate in candidates:
		index = get_insert_index(database, candidate)
		if index != -1:
			heapq.heappush(adds, [index, candidate])

	if adds:
		new_db = []
		db_index = 0
		num_adds = 0
		while adds:
			add_index, add_path = heapq.heappop(adds)
			new_db.extend(database[db_index:add_index])
			new_db.append([add_path, "1"])
			db_index = add_index
		new_db.extend(database[db_index:])
		database = new_db
	update_database(database)


def remove_path(database, path):
	index = bisect.bisect(database, [path, ""])

	if index >= len(database) or database[index][0] != path:
		print("\n\tERROR: Path Not Found")
		return

	database.pop(index)
	update_database(database)


def increment_popularity(database, index):
	assert 0 <= index < len(database)
	database[index][1] = str(int(database[index][1]) + 1)
	update_database(database)


def get_last_output():
	with open(settings.SELECTED_FILE) as infile:
		print(infile.read())


def all_paths_exist(database, paths):
	path_exists = lambda x: os.path.exists(x) or x.startswith("https://") or x.startswith("Application: ")

	all_exist = True
	for path in paths:
		if not path_exists(path):
			remove_path(database, path)
			all_exist = False
	return all_exist


def align_keyword(path, keyword):
	keyword = remove_chars(keyword)
	path = remove_chars(path)

	prev_col = [0] * (len(keyword) + 1)
	current_column = [0]

	path_del_penalty = -1
	keyword_del_penalty = -2

	score = 0

	i = 0
	for p_char in path:
		i += 1
		j = 0
		for k_char in keyword:
			j += 1
			path_del = prev_col[j] + path_del_penalty
			keyword_del = current_column[-1] + keyword_del_penalty
			match = match_score(p_char, k_char) + prev_col[j-1]

			local_score = max(0, path_del, keyword_del, match)
			current_column.append(local_score)
			score = max(local_score, score)

		prev_col = current_column
		current_column = [0]
	return score


def get_top_hits(database, keywords, num_hits=3):
	dir_hit = None
	heap = []
	for index, (path, pop) in enumerate(database):
		path = path.strip()
		pop = int(pop.strip())

		score = 0
		for keyword in keywords:
			keyword_score = align_keyword(path, keyword)
			score = max(keyword_score+score, score)

		path_node = (score, pop, -len(path), index, path)		
		heapq.heappush(heap, path_node)

		path_node = path_node[:1] + path_node[2:] + path_node[1:2]
		if not dir_hit or ((os.path.isdir(path) or path.startswith("https://")) and dir_hit < path_node):
			dir_hit = path_node
		if len(heap) > num_hits:
			heapq.heappop(heap)

	heap = sorted(heap, reverse=True)
	paths = [(item[-2:]) for item in heap]
	
	dir_hit = dir_hit[2:4] if dir_hit else None
	if dir_hit and dir_hit not in paths:
		paths[-1] = dir_hit

	return paths


def search(keywords):
	database = get_database()

	paths = None
	while paths is None or not all_paths_exist(database, paths):
		hits = get_top_hits(database, keywords)
		paths = [hit[1] for hit in hits]

	print()
	for index, path in enumerate(paths):
		print(f"\t{index+1}.) {path}")
	print()

	choice = ""
	while not choice.isnumeric() or not (0 < int(choice) <= len(hits)):
		choice = input("\tSelect Directory: ")
		if not choice:
			print()
			exit(2)
	print()
	choice = int(choice)

	chosen_index, chosen_path = hits[choice - 1]
	increment_popularity(database, chosen_index)

	with open(settings.SELECTED_FILE, 'w') as outfile:
		outfile.write(chosen_path)


if __name__ == "__main__":
	args = sys.argv
	os.chdir(os.path.dirname(args[0]))
	
	assert len(args) >= 2
	if args[1] == 'add_path':
		assert len(args) == 3
		add_path(args[2])
	elif args[1] == 'search':
		assert len(args) == 3
		keys = args[2].split()
		search(keys)
	elif args[1] == 'get_output':
		get_last_output()
	elif args[1] == 'delete':
		assert len(args) == 3
		db = get_database()
		remove_path(db, args[2])
	else:
		raise AssertionError("Invalid Option")

