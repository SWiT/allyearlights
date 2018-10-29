# allyearlights 
Controlling WS2811 LED strips using Rpi0w. The eventual goal is to leave the decorative lights up all year long with and editable schedule of color patterns for given holidays.

- Wire the WS2811 to pin 12 PWM0 on the Raspberry Pi 0

- Disable the bcm2835 sound. The timer is used to drive the WS2811.
```
sudo nano /etc/modprobe.d/snd-blacklist.conf
```

Add
`blacklist snd_bcm2835`

- Edit config.txt and add:
```
	hdmi_force_hotplug=1
	hdmi_force_edid_audio=1
```	

Or
```
sudo raspi-config
```
Force hdmi audo under "Advanced Options"->"Audio", Set password, timezone, hostname, wifi, and enable SSH.
```
sudo reboot
```

- Prerequisites
```
sudo apt update && sudo apt full-upgrade -y	
sudo apt install scons git screen python-pip
sudo pip install flask
sudo reboot
```
```
sudo apt install scons
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
sudo /home
```

- Install python lib.
```
cd python
sudo apt-get install python-dev swig 
sudo rm -rf ./build
python ./setup.py build
sudo python setup.py install
```

- Add start up script to:
```
sudo nano /etc/rc.local
```
Add:
```
/home/pi/allyearlights/startlights.sh &
```

- Edit Startup Script if you want to see output and errors
```
nano  /home/pi/allyearlights/startlights.sh
```

- Start or Stop Script
```
sudo python /home/pi/allyearlights/allyearlights.py -c
sudo pkill -ef allyearlights.py
```

