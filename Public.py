import sys
import os
import math
import time

# ------------------------------------------------------------------------
class Public(object):

    majorlist = (10,) #positioning floor
    N_LESCAN = 4 #scan 4 times by step
    serverAddr = "http://140.113.86.143:8090/"
    steplength = 0.60
    refbaro = 993.76 #barometer default ref. value
    mybeaconID = 1 #my client id
    b_UUID = "e2c56db5dffb48d2b060d0f5a71096e0"
    txPower = -60
