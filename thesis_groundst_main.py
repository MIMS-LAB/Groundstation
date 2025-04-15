import sys

sys.path.append(r"D:\alessandro\Thesis\Onboard-Firmware\include\rrc_encoder\src")
sys.path.append(r"C:\Users\RUMIM\AppData\Roaming\Python\Python312\site-packages")

import serial 
import rrc_decoder as d
import time as t

rxport= "COM7"
baud  = 9600
 
while True:

    try:
        rx_ser =  d.radioConnection(rxport, baud)
        break
    except Exception as e:
        print(e)
        exit(-1)

print("Connected")


while True:
    #rx_ser.sendCommand("a") 
    #t.sleep(1)
    data= rx_ser.readString()

    if data == None:
        t.sleep(1)

        print("none type error")
        continue
    else:
        #data_str= data.split(',')


        print(data)
    #t.sleep(1)

    
rx_ser._RadioSerialBuffer.close()
