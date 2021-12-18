# scripts
viriety of helpful scripts

## knigavuhe

A simple python v.3 script which attempts to download audio files from 
https://knigavuhe.org/

### arguments:
-  --book __BOOK__  _book url_
-  --path __PATH__  _output directory_

### example:
```
./knigavuhe.py --book "https://knigavuhe.org/book/evgenijj-onegin" --path ~/Music/EvgeniyOnegin
```
This comand downloads and parses cover page to find audio files, creates output directory EvgeniyOnegin if it doesn't exist and downloads mp3 audio files with their original names.

This script might fail for some books, particularly those referenced to litres. I might improve it when/if it becomes necesary for my personal needs. Otherwise feel free to use it at your own risk and contribute with pull requests or suggestions as you wish.


## xmas-lights

A script to run X-Mas Lights with Raspberry PI and a set of relays connected to IO pins.

The scrypt is written with asyncio and gpiozero.

The hardcoded schedule is to activate the lights between 15:00 to 01:00, it's randomised +/- 15min every day. It's set for 3 IO pins 17, 22 and 27. The 17 is always ON as in my setup these lights have their own flashing logic in its power suply. The pins 22 and 27 run a relatively slow random rhyme in counter phase. My attempt at Jingle Bells rhyme is provided (free of royalty :).

It should be obvious how to customise the schedule, the pins and the rhymes in the script, so I did not bother with the command line options for this script.

I used ubuntu desktop for writing and testing this script using mock pin factory. Use systemd and possibly /etc/rc.local to deploy on Raspberry PI.

### example:
```
copy xmas-lights.py to pi home directory -> /home/pi/xmas-lights.py

run command:
sudo vi /etc/rc.local

add 2 lines somewhere close to the end of the file but before exit 0 line.

echo "Switch-on X-Mas Lights"
/home/pi/xmas-lights.py &

save and exit.

run commands:
sudo systemctl stop rc.local
sudo systemctl start rc.local
or
sudo systemctl restart rc.local
```
