#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import subprocess
import os
import signal
import sys


GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.IN, pull_up_down=GPIO.PUD_UP)    #pin12

buttonPress = False
state = 0


while True:
	inputValue = GPIO.input(18)
	if inputValue == False :
		if buttonPress == False:
			print("Button Pressed!!")
			if state == 0:
				p = subprocess.Popen(["sh","./run.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid) 
				print "program pid",p.pid," start!!"
			else:
				if p.pid is None :
					pass
				else:
					os.killpg(os.getpgid(p.pid),signal.SIGTERM)
					print "program pid",p.pid," stop!!"
			state = ~state;
		buttonPress = True 
		time.sleep(0.2)
	else:
		buttonPress = False
