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


def check_step():
    scale = 0.92
    #com_x_offset = -209
    #com_y_offset = -106
    com_x_offset = 3
    com_y_offset = -376
    #acc_z_offset = -2500
    acc_z_offset = -500

    normList = [0] * 4
    averageList = [0] * 3
    total = 0
    lasttime = 0

    while 1:
        global counter, steplength;
        for i in xrange(12):
            accel_xout = read_word_2c(addrMPU, 0x3b) / 16384.0
            accel_yout = read_word_2c(addrMPU, 0x3d) / 16384.0
            accel_zout = (read_word_2c(addrMPU, 0x3f) - acc_z_offset) / 16384.0

            total -= normList[i % 4]
            normList[i % 4] = math.sqrt(accel_xout * accel_xout + accel_yout * accel_yout + accel_zout * accel_zout)
            total += normList[i % 4]
            average = total / 4
            averageList[i % 3] = average
"""
            output_str = '{0:3.2f}, {1:3.2f}, {2:3.2f}'.format(averageList[(i- 2) % 3],averageList[(i - 1) % 3],averageList[(i) % 3])
            sys.stdout.write(output_str+'\n')
            sys.stdout.flush()
            time.sleep(0.1)
"""

            if averageList[(i - 1) % 3] < averageList[(i - 2) % 3] and averageList[(i - 1) % 3] < averageList[(i) % 3] and averageList[(i - 1) % 3] < 1:
                cur_time = time.time()
                if cur_time - lasttime > 0.25:
                    # step detect
                    counter += 1

                    lasttime = cur_time
                    x_out = (read_word_2c(addrHMC, 3) - com_x_offset) * scale
                    y_out = (read_word_2c(addrHMC, 7) - com_y_offset) * scale
                    z_out = read_word_2c(addrHMC, 5) * scale

                    bearing = math.atan2(y_out, x_out)
                    if (bearing < 0): #change compass to polar coordinates
                        bearing += 2 * math.pi
                    bearing = 2 * math.pi - bearing

                    imuString = 'I ' + str(time.time()) + ' ' + str(steplength) + ' ' + str(bearing) + ' '
                    sys.stdout.write(imuString+'\n')
                    sys.stdout.flush()



def main():

    #imu event
    imuString = 'I ' + str(time.time()) + ' 0 0 '
    #print imuString
    sys.stdout.write(imuString+'\n')
    sys.stdout.flush()

    init_imu()
   #handle location result
    lasttime = time.time()
    #thread.start_new_thread(writeUrlQueue, ())

    check_step()

if __name__ == "__main__":
    main()
