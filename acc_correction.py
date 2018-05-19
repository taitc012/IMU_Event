#!/usr/bin/env python
import uuid 
import sys, os, math, time, thread, smbus, random, requests
import Queue
from signal import signal, SIGPIPE, SIG_DFL
from Public import Public 
# Power management registers

signal(SIGPIPE, SIG_DFL)
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

bus = smbus.SMBus(1)
addrMPU = 0x68
addrHMC = 0x1e


serverAddr = Public.serverAddr
steplength = Public.steplength
counter = 0 #count step#
lasttime = 0.0
lastsendtime = 0.0


def init_imu():
    # Now wake the MPU up as it starts in sleep mode
    bus.write_byte_data(addrMPU, power_mgmt_1, 0)

    # HMC setting
    bus.write_byte_data(addrHMC, 0, 0b01110000)  # Set to 8 samples @ 15Hz
    bus.write_byte_data(addrHMC, 1, 0b00100000)  # 1.3 gain LSb / Gauss 1090 (default)
    bus.write_byte_data(addrHMC, 2, 0b00000000)  # Continuous sampling


def read_byte(address, adr):
    return bus.read_byte_data(address, adr)


def read_word(address, adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low
    return val


def read_word_2c(address, adr):
    val = read_word(address, adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


def main():
    init_imu()
    while True:
        #accel_xout = read_word_2c(addrMPU, 0x3b) / 16384.0
        #accel_yout = read_word_2c(addrMPU, 0x3d) / 16384.0
        #accel_zout = read_word_2c(addrMPU, 0x3f) / 16384.0
        acc_x = read_word_2c(addrMPU, 0x3b)
        acc_y = read_word_2c(addrMPU, 0x3d)
        acc_z = read_word_2c(addrMPU, 0x3f)
        x_offset = 0;
        y_offset = 0;
        z_offset = 17000;
        """
        accel_xout = (acc_x-x_offset) / 16384.0
        accel_yout = (acc_y-y_offset) / 16384.0
        accel_zout = (acc_z-z_offset) / 16384.0
        accel_xout = acc_x - x_offset
        accel_yout = acc_y - y_offset
        accel_zout = acc_z - z_offset
        """
        accel_xout = acc_x
        accel_yout = acc_y
        accel_zout = acc_z

        output_str = 'x: {0:3.2f}, y: {1:3.2f}, z: {2:3.2f}'.format(accel_xout,accel_yout, accel_zout)
        sys.stdout.write(output_str+'\n')
        sys.stdout.flush()
        time.sleep(0.2)


if __name__ == "__main__":
    main()
