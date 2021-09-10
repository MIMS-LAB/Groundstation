####    imports    ####

import sys

sys.path.insert(1, "E:/RRC/Library-RRC-encoder/src")
sys.path.append(
    "C:/Users/MIMS-PC/AppData/Local/Programs/Python/Python39/Lib/site-packages")

import rfd900p as rfd
import os
import random
import time as t
import rrc_decoder as d


####    test setup    ####

TX_PORT = "COM10"           # encoder transmitting port
RX_PORT = "COM4"           # decoder recieving port
BAUD = "57600"           # baudrate
TEST = d.RRC_HEAD_GPS_LONG   # data header to test


####    encoder setup    ####

PATH    = "D:/ALESSANDRO/RRC/Library-RRC-encoder/tests" #"D:/ALESSANDRO/RRC/Groundstation-GUI-Electron/src" #"C:/Users/ahmad/OneDrive/Documents/GitHub/RRC/Library-RRC-encoder/tests"
command = PATH+"/test"
test    = lambda header, data, time : os.system(
    f"{command} {TX_PORT} {header} {data} {time}")  # encoder call lambda

# compile encoder using gcc
os.system(f"gcc {PATH}/test.c -o {command} -std=c99")


port = RX_PORT
baud = BAUD
count=0

####    initilization    ####

while True:
    try:
        radio = d.radioConnection(port, baud)

        break
    except Exception as e:
        print(e)
        exit(-1)

    print("Connected")

'''  

while radio._RadioSerialBuffer.isOpen() == True:
    initialByte = radio._readByte()
    print(initialByte)

    packets = radio.getPackets()

    if packets == None:
        print("an error happend")
        continue

    result = d.decodePackets(packets)
    print(result)

    if result["corrupted"]:
        print("CORRUPT: " + str(count))
        continue

    result.pop("checksum")
    count = count + 1

'''




####    set ranges    ####

if TEST in [d.RRC_HEAD_GPS_LAT, d.RRC_HEAD_GPS_LONG]:
    lowerRange = -1_800_000
    upperRange = 1_800_000
    multiplier = 10_000
else:
    lowerRange = -4_000
    upperRange = 4_000
    multiplier = 100


####    test for 1000 random values    ####

for i in range(1000):
    data = random.randint(lowerRange, upperRange) / multiplier
    time = random.randint(0, 0xfffff)

    test(TEST, data, time)

    packets = radio.getPackets()

    if packets == None:
        print("an error happend")
        continue

    result = d.decodePackets(packets)

    if result["corrupted"]:
        print("CORRUPT: " + str(i))
        continue

    result.pop("checksum")

    if { "header" : TEST, "data" : data, "time" : time, "corrupted" : False } == result:
        print("OK: " + str(i))
    else:
        print("ERROR: " + str(i))
    
    # print(packets)
    # print(result)
    
if __name__ == "__main__":
    print("")