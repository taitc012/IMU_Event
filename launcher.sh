#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/IMU_Event
sudo -u pi ./button.py
cd /
