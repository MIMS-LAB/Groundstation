####    imports    ####

import os, sys, random
import time as t
sys.path.insert(1, "D:\Alessandro\FILESFORSCHOOL\RRC-Avionics-master\Library-RRC-encoder\src")
import rrc_decoder as d


####    test setup    ####

TX_PORT = "COM10"           # encoder transmitting port
RX_PORT = "COM5"           # decoder recieving port
BAUD    = "57600"           # baudrate
TEST    = d.RRC_HEAD_GPS_LONG   # data header to test


####    encoder setup    ####

PATH    = "D:\Alessandro\FILESFORSCHOOL\RRC-Avionics-master\Library-RRC-encoder\tests"
command = PATH+"/test"  
test    = lambda header, data, time : os.system(f"{command} {TX_PORT} {header} {data} {time}")  # encoder call lambda

os.system(f"gcc {PATH}/test.c -o {command} -std=c99")  # compile encoder using gcc

####    initilization    ####

while True:
    port = RX_PORT
    baud = BAUD

    try:
        radio = d.radioConnection(port, baud)
        break
    except Exception as e:
        print(e)
        exit(-1)

print("Connected")





