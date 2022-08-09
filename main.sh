#!/bin/zsh

if [[ "$SHELL" == *zsh ]]; then
	dir="$(dirname "$0")"
else
	dir="$(dirname "${BASH_SOURCE[0]}")"
fi

if [[ -e "$*" || "$*" == https://* || "$*" == Application:\ * ]]; then
	dest="$("$dir/get_abs_path.sh" "$*")"
	"$dir/file_search.py" add_path --increment "$dest"
	"$dir/open" "$dest"
else
	"$dir/file_search.py" search "$*"
	if [[ $? == "0" ]]; then
		selected_path="$("$dir/file_search.py" get_output)"
		if [[ -d "$selected_path" ]]; then
			cd "$selected_path"
			if [[ -f "$c_file" && -f "$v_file" ]]; then
				cat "$v_file" > "$c_file"; c="$v"
				vs
			fi
		else
			"$dir/open" "$selected_path"
		fi
	fi
fi


