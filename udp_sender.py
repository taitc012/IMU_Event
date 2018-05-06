#!/usr/bin/env python

import socket
import sys
import getopt
import time


UDP_IP = "192.168.43.118"
UDP_PORT = 5566

try:
    opts, args = getopt.getopt(sys.argv[1:],"ha:p:",["address=","port="])
except getopt.GetoptError:
    print('./udp_sender.py [-a <server address>] [-p <server port>]')
    sys.exit(2)
    
for opt, arg in opts:
    print(opt)
    if opt == '-h':
        print('./udp_sender.py [-a <server address>] [-p <server port>]')
        sys.exit()
    elif opt in ("-a", "--address"):
        UDP_IP = arg
    elif opt in ("-p", "--port"):
        UDP_PORT = arg #int(arg)

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

while True:
    sys.stdin.flush()
    #msg = input()
    msg = raw_input()
    print(msg)
    #sock.sendto(bytes(msg+'\n', "utf-8"), (UDP_IP, UDP_PORT))
    sock.sendto(msg+'\n', (UDP_IP, UDP_PORT))
