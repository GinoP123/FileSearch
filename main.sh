#!/bin/zsh

cwd="$PWD"
cd $(dirname "$0")

./file_search.py search "$*"

if [[ $? == "0" ]]; then
	selected_path="$(./file_search.py get_output)"
	cd $selected_path
else
	cd $cwd
fi
