import sys, os, math, time, thread, smbus, random, requests
#import Adafruit_BMP.BMP085 as BMP085
import Queue
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

bus = smbus.SMBus(1)
addrMPU = 0x68
addrHMC = 0x1e

def init_imu():
    # Now wake the MPU up as it starts in sleep mode
    bus.write_byte_data(addrMPU, power_mgmt_1, 0)

    # HMC setting
    bus.write_byte_data(addrHMC, 0, 0b01110000)  # Set to 8 samples @ 15Hz
    bus.write_byte_data(addrHMC, 1, 0b00100000)  # 1.3 gain LSb / Gauss 1090 (default)
    bus.write_byte_data(addrHMC, 2, 0b00000000)  # Continuous sampling

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
    x_max = -9999
    x_min = 9999
    y_max = -9999
    y_min = 9999
    while True:
        x = read_word_2c(addrHMC, 3) 
        y = read_word_2c(addrHMC, 7)
        z = read_word_2c(addrHMC, 5)
        
        x_max = x if x_max < x else x_max
        x_min = x if x_min > x else x_min
        y_max = y if y_max < y else y_max
        y_min = y if y_min > y else y_min
        
        middle_x = (x_max + x_min)/2
        middle_y = (y_max + y_min)/2

        x_out = x - middle_x
        y_out = y - middle_y

        bearing = math.atan2(y_out, x_out)
        if (bearing < 0): #change compass to polar coordinates
            bearing += 2 * math.pi
        bearing = 2 * math.pi - bearing

        #print "x: ",x,",y: ",y,",z: ",z,"          x_max: ",x_max,",x_min: ",x_min,"y_max: ",y_max,",y_min: ",y_min
        print "x: ",x,",y: ",y,",z: ",z,"          middle_x: ",middle_x,",middle_y: ",middle_y,"      degree:",int(math.degrees(bearing))
        #print x,y
        time.sleep(0.2)

if __name__ == "__main__":
    main()
