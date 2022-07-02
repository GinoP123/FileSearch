#!/usr/bin/env python3

import heapq
import sys
import settings
import os


def remove_chars(string):
	string = string.lower()
	new_str = ''
	for char in string:
		if char not in '_/ \n\t':
			new_str += char
	return new_str


def match_score(a, b):
	return 1 if a == b else -1


def align_keyword(keyword, path):
	keyword = remove_chars(keyword)
	path = remove_chars(path)

	prev_col = [0] * (len(keyword) + 1)
	current_column = [0]

	path_del_penalty = -1
	keyword_del_penalty = -3

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


def get_lines(path):
	with open(path) as infile:
		return infile.readlines()


def get_path_pop_lines():
	return get_lines(settings.DB_FILE), get_lines(settings.POP_FILE)


def get_path_index(path, db_lines):
	path_index = -1
	for index, line in enumerate(db_lines):
		if f"{path}\n" == line:
			path_index = index
			break
	return path_index


def update_database(path, lines):
	with open(path, 'w') as outfile:
		outfile.write(''.join(lines))


def update_databases(db_lines, pop_lines):
	update_database(settings.DB_FILE, db_lines)
	update_database(settings.POP_FILE, pop_lines)


def add_path(path):
	db_lines, pop_lines = get_path_pop_lines()
	if get_path_index(path, db_lines) != -1:
		exit(2)

	db_lines.append(f"{path}\n")
	pop_lines.append(f"1\n")

	update_databases(db_lines, pop_lines)


def remove_path(path, db_lines, pop_lines):
	index = get_path_index(path, db_lines)

	if index == -1:
		print("\n\tERROR: Path Not Found")
		return

	db_lines.pop(index)
	pop_lines.pop(index)

	update_databases(db_lines, pop_lines)


def increment_popularity(index, pop_lines):
	assert 0 <= index < len(pop_lines)
	new_line = f"{int(pop_lines[index].strip()) + 1}\n"
	pop_lines[index] = new_line
	update_database(settings.POP_FILE, pop_lines)


def get_top_hits(keywords, db_lines, pop_lines, num_hits=3):
	heap = []
	for index, (path, pop) in enumerate(zip(db_lines, pop_lines)):
		path = path.strip()
		pop = int(pop.strip())

		score = 0
		for keyword in keywords:
			keyword_score = align_keyword(keyword, path)
			score = max(keyword_score+score, score)

		heapq.heappush(heap, (score, pop, -index, -len(path), path))
		if len(heap) > num_hits:
			heapq.heappop(heap)

	heap = sorted(heap, reverse=True)
	return [(-item[2], item[4]) for item in heap]


def all_paths_exist(paths, db_lines, pop_lines):
	path_exists = lambda x: os.path.isdir(x)

	all_exist = True
	for path in paths:
		if not path_exists(path):
			remove_path(path, db_lines, pop_lines)
			all_exist = False
	return all_exist


def search(keywords):
	db_lines, pop_lines = get_path_pop_lines()

	paths = None
	while paths is None or not all_paths_exist(paths, db_lines, pop_lines):
		hits = get_top_hits(keywords, db_lines, pop_lines)
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
	increment_popularity(chosen_index, pop_lines)

	with open(settings.CWD_FILE, 'w') as outfile:
		outfile.write(chosen_path)


if __name__ == "__main__":
	args = sys.argv
	if len(args) != 3:
		exit(1)

	if args[1] == 'add_path':
		add_path(args[2])
	elif args[1] == 'search':
		keys = args[2].split()
		search(keys)
	else:
		raise AssertionError("Invalid Option")


