#!/bin/bash
python3 create_deck.py
ANKI_WAYLAND=1 anki &>/dev/null  &  
git status

read -p "Do you want to continue? (y/n): " choice

case "$choice" in 
	y|Y ) git add  .; git commit -m "$(date)"; git push ;;
  n|N ) echo "Exiting..."; exit 1;;
  * ) echo "Invalid input. Please enter y or n."; exit 1;;
esac
