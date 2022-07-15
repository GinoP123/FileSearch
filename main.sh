#!/bin/zsh

if [[ "$SHELL" == *zsh ]]; then
	dir="$(dirname "$0")"
else
	dir="$(dirname "${BASH_SOURCE[0]}")"
fi

if [[ -e "$*" || "$*" == https://* ]]; then
	. "$dir/open_add_path.sh" "$("$dir/get_abs_path.sh" "$*")"
else
	"$dir/file_search.py" search "$*"
	if [[ $? == "0" ]]; then
		selected_path="$("$dir/file_search.py" get_output)"
		if [[ -d "$selected_path" ]]; then
			cd "$selected_path"
		else
			"$dir/open" "$selected_path"
		fi
	fi
fi


