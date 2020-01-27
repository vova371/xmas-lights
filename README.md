# scripts
viriety of helpful scripts

##knigavuhe

A simple python v.3 script which attempts to download audio files from 
https://knigavuhe.org/

###arguments:
  --book BOOK  book url
  --path PATH  output directory

###example:
./knigavuhe.py --book "https://knigavuhe.org/book/evgenijj-onegin" --path ~/Music/EvgeniyOnegin

This comand downloads and parses cover page to find audio files, creates output directory EvgeniyOnegin if it doesn't exist and downloads mp3 audio files with their original names.

This script might fail for some books, particularly those referenced to litres. I might improve it when/if it becomes necesary for my personal needs. Otherwise feel free to use it at your own risk and contribute with pull requests or suggestions as you wish.
