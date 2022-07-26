#!/bin/bash

dir="$(dirname "$0")"
cd "$dir"

# Making text files dir and database
mkdir -p "text_files"
touch "text_files/database.csv"
echo -e "\n\tDatabase Setup Complete!\n"


# Adding Aliases
ls_alias="alias ls='$PWD/file_search.py add_path \$PWD; ls'"
o_alias="alias o='. $PWD/main.sh'"
delete_alias="alias delete='$PWD/delete_path.sh'"

if [[ ! -f "open" ]]; then
	alias_path="$HOME/.bashrc"
	if [[ "$SHELL" == *zsh ]]; then
		alias_path="$HOME/.zshrc"
	fi

	echo "" >> "$alias_path"
	echo "# Aliases for FileSearch" >> "$alias_path"
	echo "$ls_alias" >> "$alias_path"
	echo "$o_alias" >> "$alias_path"
	echo "$delete_alias" >> "$alias_path"
	echo "" >> "$alias_path"
	
	echo -e "\n\tAdded Aliases to $alias_path\n\n"
	echo -e "\tMake sure to source $alias_path after!\n"
fi

open_path="/"
while [[ "$open_path" != "" && ! -f "$open_path" ]];
do
	read -p $'\n\t'"Path to File Opener (default: /usr/local/bin/sublime): " open_path
done

# Settings sym link to open
if [[ "$open_path" == "" ]]; then
	open_path="./sublime.sh"
fi

rm -f "open"
ln -s "$open_path" "open"

echo -e "\n\tSet File Editor to $open_path\n"

echo -e "\n\tFinished Setup!"



