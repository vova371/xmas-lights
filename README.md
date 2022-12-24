# xmas-lights

A script to run X-Mas Lights with Raspberry PI and a set of relays connected to IO pins.

The scrypt is written with asyncio and gpiozero.

The hardcoded schedule is to activate the lights between 15:00 to 01:00, it's randomised +/- 15min every day. It's set for 3 IO pins 17, 22 and 27. The 17 is always ON as in my setup these lights have their own flashing logic in its power suply. The pins 22 and 27 run a relatively slow random rhyme in counter phase. My attempt at Jingle Bells rhyme is provided (free of royalty :).

It should be obvious how to customise the schedule, the pins and the rhymes in the script, so I did not bother with the command line options for this script.

The logfile is created in the same directory as the running script with name xmas-lights.log.

### Tip 1
Use mock pin factory for testing xmas-lights.py script on machine without IO pins.

```
GPIOZERO_PIN_FACTORY=mock xmas-lights.py
```

### Tip 2
Use systemd and optionally /etc/rc.local to deploy on Raspberry PI.

```
copy xmas-lights.py to pi home directory -> /home/pi/xmas-lights.py

run command:
sudo vi /etc/rc.local

add 2 lines somewhere close to the end of the file but before the exit command.

echo "Switch-on X-Mas Lights"
/home/pi/xmas-lights.py &

save and exit.

run commands:
sudo systemctl restart rc.local
```

Raspberry PI  ->  5V Four-Channel Relay Module

| Pin | Name   | Pin | Colour |
|-----|--------|-----|--------|
|2    |5V power|VCC  | Red    |
|6    |Ground	 |GND  | Black  |
|11   |GPIO 17 |IN1  | Orange |
|13   |GPIO 27 |IN2  | Yellow |
|15   |GPIO 22 |IN3  | Green  |

Normally Closed (NC) 240V Relay Connections

| Connection | Description                    | Usage             |
|------------|--------------------------------|-------------------|
| Relay 1    | Schedulled ON/OFF              | Rainfall & Wreath |
| Relay 2    | Schedulled Random Counterphase | Snowflake         |
| Relay 3    | Schedulled Random Main phase   | Bells             |


https://components101.com/switches/5v-four-channel-relay-module-pinout-features-applications-working-datasheet
https://www.raspberrypi.com/documentation/computers/remote-access.html
