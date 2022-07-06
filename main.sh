#!/bin/zsh

cwd="$PWD"
cd $(dirname "$0")

./file_search.py search "$*"

if [[ $? == "0" ]]; then
	selected_path="$(./file_search.py get_output)"

	if [[ -d "$selected_path" ]]; then
		cd "$selected_path"
	else
		./open "$selected_path"
	fi
else
	cd "$cwd"
fi

unset cwd

