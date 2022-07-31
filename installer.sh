#!/bin/bash

cd "$(dirname "$0")"

# Making text files dir and database
mkdir -p "text_files"
touch "text_files/database.csv"
touch "text_files/current_count.txt"
touch "text_files/database_sizes.csv"
echo -e "\n\tDatabase Setup Complete!\n"

# Adding Aliases
source_line="export PATH='$PWD/bin:\$PATH'"
o_alias="alias o='. $PWD/main.sh'"


if [[ ! -f "open" ]]; then
	alias_path="$HOME/.bash_profile"
	if [[ "$SHELL" == *zsh ]]; then
		alias_path="$HOME/.zprofile"
	fi

	echo "" >> "$alias_path"
	echo "# Setting PATH for FileSearch " >> "$alias_path"
	echo "$source_line" >> "$alias_path"
	echo "$o_alias" >> "$alias_path"
	echo "" >> "$alias_path"
	
	echo -e "\n\tAdded Aliases to $alias_path\n\n"
	echo -e "\tMake sure to source $alias_path after!\n"
fi

ls_path="$(which ls)"
echo $ls_path
if [[ "$ls_path" != */FileSearch/bin/ls ]]; then
	default_ls_path="/bin/ls"
	cat bin/ls | sed "s,$default_ls_path,$ls_path," > bin/ls
fi


open_path="/"
while [[ "$open_path" != "" && ! -f "$open_path" ]]
do
	read -p $'\n\t'"File Opener(name or path) (default: vim): " open_path

	if [[ "$open_path" == "" ]]; then
		open_path="vim"
	fi
	open_path="$(which "$open_path")"
done

rm -f "open"
ln -s "$open_path" "open"

echo -e "\n\tSet File Editor to $open_path\n"

echo -e "\n\tFinished Setup!\n"



