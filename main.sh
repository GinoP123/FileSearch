#!/bin/zsh

cwd=$PWD
dir=$FILE_SEARCH_DIR
cd $dir

script=$(python3 -c "import settings; print(settings.SCRIPT_FILE)")
output=$(python3 -c "import settings; print(settings.CWD_FILE)")
cd $cwd

$script search "$*"

if [[ $? == "0" ]]; then
	cd $(cat $output)
fi
