#!/usr/bin/env python3

import sys
import os
import heapq
import csv
import bisect
import settings


def remove_chars(string):
	string = string.lower()
	new_str = ''
	for char in string:
		if char not in '_/ \n\t':
			new_str += char
	return new_str


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
		if len(siblings) > settings.neighbor_limit:
			return list({dirname, path})
		return [dirname] + siblings
	return [path]


def get_insert_index(database, path):
	index = bisect.bisect(database, [path, '', '', ''])
	if index >= len(database) or database[index][settings.PATH_IND] != path:
		return index
	return -1


def get_shift(string1, string2):
	shift = 0
	for ch1, ch2 in zip(string1, string2):
		if ch1 == ch2:
			shift += 1
		else:
			break
	return str(shift)


def update_shift(database=None, index=-1):
	if database and len(database) > index:
		if index:
			string1 = remove_chars(database[index - 1][settings.PATH_IND])
		else:
			string1 = ''
		string2 = remove_chars(database[index][settings.PATH_IND])
		database[index][settings.SHIFT_IND] = get_shift(string1, string2)


def get_path_type(path):
	if os.path.isdir(path):
		return 'd'
	elif path.startswith(settings.url_prefix):
		return 'l'
	elif path.startswith(settings.app_prefix):
		return 'a'
	else:
		return 'f'


def add_paths(candidates):
	database = get_database()
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
			update_shift(new_db, db_index + num_adds)

			path_type = get_path_type(add_path)
			new_db.append([add_path, path_type, "0", "1"])
			update_shift(new_db, add_index + num_adds)

			db_index = add_index
			num_adds += 1

		new_db.extend(database[db_index:])
		update_shift(new_db, db_index + num_adds)
		database = new_db
	update_database(database)


def remove_path(database, path):
	index = bisect.bisect(database, [path, '', '', ''])
	if index >= len(database) or database[index][settings.PATH_IND] != path:
		print("\n\tERROR: Path Not Found")
		return

	database.pop(index)
	update_shift(database, index)
	update_database(database)


def increment_popularity(database, index):
	assert 0 <= index < len(database)
	database[index][settings.POP_IND] = str(int(database[index][settings.POP_IND]) + 1)
	update_database(database)


def get_last_output():
	with open(settings.SELECTED_FILE) as infile:
		print(infile.read())


def all_paths_exist(database, paths):
	path_exists = lambda x: os.path.exists(x) or get_path_type(x) in 'la'

	all_exist = True
	for path in paths:
		if not path_exists(path):
			remove_path(database, path)
			all_exist = False
	return all_exist


def align_keyword(path, keyword, memo=[], shift=0):
	keyword = remove_chars(keyword)
	path = remove_chars(path)
	shift = int(shift)

	while len(memo) < len(path) + 1:
		memo.append([0] * (len(keyword) + 2))

	path_del_penalty = -1
	keyword_del_penalty = -2

	columns = range(shift+1, len(path)+1)
	for curr_col, p_char in zip(columns, path[shift:]):
		for j, k_char in enumerate(keyword):
			path_del = memo[curr_col-1][j+1] + path_del_penalty
			keyword_del = memo[curr_col][j] + keyword_del_penalty
			match = (1 if p_char == k_char else -1) + memo[curr_col-1][j]
			local_score = max(0, path_del, keyword_del, match)
			memo[curr_col][j+1] = local_score
			memo[curr_col][-1] = max(local_score, memo[curr_col-1][-1])
	return memo[len(path)][-1]


def get_top_hits(database, keywords, num_hits=3):
	dir_hit = None
	memo_list = [[] for _ in keywords]
	heap = []
	for index, (path, ptype, shift, pop) in enumerate(database):
		path = path.strip()
		score = 0
		for memo, keyword in zip(memo_list, keywords):
			score += align_keyword(path, keyword, memo, shift)

		path_node = (score, pop, -len(path), index, path)		
		heapq.heappush(heap, path_node)

		path_node = path_node[:1] + path_node[2:] + path_node[1:2]
		if not dir_hit or ((ptype != 'f') and dir_hit < path_node):
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
		choice = input("\tSelect Path: ")
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
		add_paths(get_neighboring_paths(args[2]))
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

