#!/bin/bash

cd "$(dirname "$0")"

# Making text files dir and database
mkdir -p "text_files"
touch "text_files/database.csv"
touch "text_files/current_count.txt"
touch "text_files/database_sizes.txt"
echo -e "\n\tDatabase Setup Complete!\n"

# Adding Aliases
source_line="export PATH=\"$PWD/bin:\$PATH\""
o_alias="alias o='. $PWD/main.sh'"
mini_bookmark_source="source '$PWD/mini_bookmarks.sh'"
c_file="$PWD/text_files/c_file.txt"
v_file="$PWD/text_files/v_file.txt"


if [[ ! ( -f "open" && -f "$c_file" && -f "$v_file" ) ]]; then
	alias_path="$HOME/.bash_profile"
	if [[ "$SHELL" == *zsh ]]; then
		alias_path="$HOME/.zprofile"
		cp bin/x_zsh bin/x
	else
		cp bin/x_bash bin/x
	fi

	if [[ ! -f "open" ]]; then
		echo "" >> "$alias_path"
		echo "# Setting PATH for FileSearch " >> "$alias_path"
		echo "$source_line" >> "$alias_path"
		echo "$o_alias" >> "$alias_path"
	fi
	
	if [[ ! ( -f "$c_file" && -f "$v_file" ) ]]; then
		input=""
		while [[ $input != 'y' && $input != 'n' ]]
		do
			read -p $'\n\t'"Install Mini Bookmarks?: " input
		done

		if [[ "$input" == 'y' ]]; then
			echo "$mini_bookmark_source" >> "$alias_path"
			touch "$c_file"
			touch "$v_file"
		fi
	fi

	if [[ ! -f "open" || $input == 'y' ]]; then
		echo "" >> "$alias_path"
		echo -e "\n\tAdded Aliases to $alias_path\n\n"
		echo -e "\tMake sure to source $alias_path after!\n"
	fi
fi




ls_path="$(which ls)"
if [[ "$ls_path" != */FileSearch/bin/ls ]]; then
	default_ls_path="/bin/ls"
	cat bin/ls | sed "s,$default_ls_path,$ls_path," > bin/tmp_ls
	cat bin/tmp_ls > bin/ls
	rm bin/tmp_ls
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



