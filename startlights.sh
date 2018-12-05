#!/bin/bash
sudo python /home/pi/allyearlights/allyearlights.py -c > /dev/null 2>&1 &
sudo python /home/pi/allyearlights/allyearlights-web.py > /dev/null 2>&1 &
