# allyearlights 
Controlling WS2811 LED strips using Rpi0w. The eventual goal is to leave the decorative lights up all year long with and editable schedule of color patterns for given holidays.

>WS2811 on pin 12 PWM0

`sudo nano /etc/modprobe.d/snd-blacklist.conf`
`Add:
	blacklist snd_bcm2835
`	
`Edit config.txt and add:
	hdmi_force_hotplug=1
	hdmi_force_edid_audio=1
`	
Or
>force hdmi audo via raspi-config under "Advanced Options"->"Audio"

Set password, timezone, hostname, wifi, and enable SSH.
```
sudo raspi-config	
sudo reboot

sudo apt update && sudo apt full-upgrade -y	
sudo apt install scons git screen
sudo reboot

sudo apt install scons
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
sudo /home

#Install python lib.
cd python
sudo apt-get install python-dev swig
sudo rm -rf ./build
python ./setup.py build
sudo python setup.py install

#Add start up script to:
sudo nano /etc/rc.local
#Add:
#	/home/pi/startup.sh &

nano  /home/pi/startup.sh
#!/bin/bash
/home/pi/rpi_ws281x/test -x 150 -y 1 -c &
#or
python /home/pi/blink.py -c &

ps aux | grep test
kill -s SIGINT [PID]
```

