#!/bin/zsh

cwd="$PWD"

if [[ "$SHELL" == *zsh ]]; then
	cd "$(dirname "$0")"
else
	cd "$(dirname "${BASH_SOURCE[0]}")"
fi

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

