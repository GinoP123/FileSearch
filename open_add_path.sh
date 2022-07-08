#!/bin/zsh

file_search_dir="$(dirname "$0")"
dest=$("$file_search_dir/get_abs_path.sh" "$1")
"$file_search_dir/file_search.py" add_path "$dest"
"$file_search_dir/open" "$dest"
