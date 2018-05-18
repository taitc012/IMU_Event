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
                p1 = subprocess.Popen(['ssh','nmslab@csi-transmitter',"sudo /home/nmslab/linux-80211n-csitool-supplementary/injection/random_packets 100000 100 1 50000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid) 
                print "program pid",p1.pid," start!!"
                p2 = subprocess.Popen(['sh','./run.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid) 
                print "program pid",p2.pid," start!!"
            else:
                if p1.pid is None :
                    pass
                else:
                    os.killpg(os.getpgid(p1.pid),signal.SIGTERM)
                    print "program pid",p1.pid," stop!!"

                if p2.pid is None :
                    pass
                else:
                    os.killpg(os.getpgid(p2.pid),signal.SIGTERM)
                    print "program pid",p2.pid," stop!!"
                    p3 = subprocess.Popen(['ssh','nmslab@csi-transmitter',"ps -u root | grep random_packets | awk '{print $1}'| xargs sudo kill"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid) 
            state = ~state;
        buttonPress = True 
        time.sleep(0.2)
    else:
        buttonPress = False
