#!/usr/bin/env python3

import heapq
import sys
import settings


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


def add_path(path):
	with open(settings.DB_FILE) as infile:
		if f"{path}\n" in infile.readlines():
			return

	with open(settings.DB_FILE, 'a') as outfile:
		outfile.write(f"{path}\n")
	with open(settings.POP_FILE, 'a') as outfile:
		outfile.write(f"1\n")


def increment_popularity(index, pop_lines):
	assert 0 <= index < len(pop_lines)
	new_line = f"{int(pop_lines[index].strip()) + 1}\n"
	with open(settings.POP_FILE, 'w') as outfile:
		for line in pop_lines[:index]:
			outfile.write(line)

		outfile.write(new_line)

		for line in pop_lines[index+1:]:
			outfile.write(line)


def get_top_hits(keywords, pop_lines, num_hits=3):
	heap = []
	db_file = open(settings.DB_FILE)

	for index, (path, pop) in enumerate(zip(db_file, pop_lines)):
		pop = int(pop.strip())

		score = 0
		for keyword in keywords:
			keyword_score = align_keyword(keyword, path)
			score = max(keyword_score+score, score)

		heapq.heappush(heap, (score, pop, -index, -len(path), path))
		if len(heap) > num_hits:
			heapq.heappop(heap)
	db_file.close()

	heap = sorted(heap, reverse=True)
	return [(-item[2], item[4]) for item in heap]


def search(keywords):
	with open(settings.POP_FILE) as infile:
		pop_lines = infile.readlines()

	hits = get_top_hits(keywords, pop_lines)

	print()
	for index, hit in enumerate(hits):
		path = hit[1]
		print(f"\t{index+1}.): {path}", end='')
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


