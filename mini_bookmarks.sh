#!/bin/bash

if [[ "$SHELL" == *zsh ]]; then
	dir="$(dirname "$0")"
else
	dir="$(dirname "${BASH_SOURCE[0]}")"
fi

c_file="$dir/text_files/c_file.txt"
v_file="$dir/text_files/v_file.txt"

if [[ -e "$c_file" && -e "$v_file" ]]; then
	c="$(cat "$c_file")"
	v="$(cat "$v_file")"

	alias c="cd \"\$(cat \$c_file)\""
	alias v="cd \"\$(cat \$v_file)\""

	alias cs='echo $PWD > $c_file; c="$PWD"'
	alias vs='echo $PWD > $v_file; v="$PWD"'
fi
