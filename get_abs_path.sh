#!/bin/zsh

if [[ "$1" == https://* ]]; then
	echo "$1"
	exit 0
fi

dest=$(dirname "$1")

if [[ "$dest" != */ ]]; then
	dest="$dest/"
fi

if [[ $dest == ./* ]]; then
	dest="$PWD/${dest:2}"
elif [[ $dest != /* ]]; then
	dest="$PWD/$dest"
fi

base=$(basename "$1")

if [[ $base == '.' ]]; then
	base=""
fi

dest="$dest$base"

if [[ $dest == */ ]]; then
	dest="${dest%?}"
fi

echo "$dest"

