#!/bin/zsh

fs_script="$(dirname "$0")/file_search.py"
"$fs_script" search "$*"

if [[ $? == "0" ]]; then
	selected_path="$("$fs_script" get_output)"
	"$fs_script" "delete" "$selected_path"
	echo -e "\tDELETED $selected_path\n"
fi

