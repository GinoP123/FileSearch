#!/bin/zsh

#!/bin/zsh

if [[ "$SHELL" == *zsh ]]; then
	dir="$(dirname "$0")"
else
	dir="$(dirname "${BASH_SOURCE[0]}")"
fi

"$dir/file_search.py" search "$*"

if [[ $? == "0" ]]; then
	selected_path="$("$dir/file_search.py" get_output)"
	"$dir/file_search.py" "delete" "$selected_path"
	echo -e "\tDELETED $selected_path\n"
fi

