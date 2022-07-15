#!/bin/zsh

if [[ "$SHELL" == *zsh ]]; then
	file_search_dir="$(dirname "$0")"
else
	file_search_dir="$(dirname "${BASH_SOURCE[0]}")"
fi

dest=$("$file_search_dir/get_abs_path.sh" "$*")
"$file_search_dir/file_search.py" add_path "$dest"
"$file_search_dir/open" "$dest"
