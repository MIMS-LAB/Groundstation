'''
This file relates to sending commands to flight contorller to control servos via pc and not frsky taranis controller

'''

import sys
# this is where python stores modules, yours could be different
sys.path.append(r"D:/Alessandro/python39/Lib/site-packages")

import time
#import cv2
import serial
import rrc_decoder as d
import numpy as np
RX_PORT = 'COM4'
rx_connect = False
baud = 57600

rxLg_flag = False
rxSm_flag = False
####    initilization    ####
count = 0
servo_header = []
hcount = []
hFlag = False
while True:

    port = RX_PORT
    baud = baud

    try:
        '''
        ser_rx = serial.Serial(
            port=port,
            baudrate=baud,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.EIGHTBITS,xonxoff=True,
            timeout=None)
        '''
        ser_rx = d.radioConnection(port, baud)
        rx_connect = True
        break
    except Exception as f:
        print(f)
        rx_connect = False
        exit(-1)
print(" connected to: " + ser_rx._RadioSerialBuffer.portstr)

while rx_connect == True:
    print("********************** count %d:*********************** \n" % count)
    
    servo_str= ser_rx.readString()#_RadioSerialBuffer.read(byteInWait).strip().decode("utf-8")    # write a string
    
    
    time.sleep(10)


    if (servo_str  == None): # if entire read string is None then somethings wrong and reparse serial buffer
        print("HE0: packet None type error! \n")
        continue
    servo_str.replace('\x00','')
    servo_header = servo_str.strip().split('\n') # split str into  array to parse through just incase we read 2 headers at once

    for i in range(0,len(servo_header)):
        header_test = servo_header[i]
        if (header_test == "Sm"):
            rxSm_flag = True
            servo1_headerFlag=i+1
        if (header_test == "Lg"):
            rxLg_flag = True
            servo2_headerFlag=i+1
        if (header_test == '\x00'):
            servo_header.replace('\x00','')

   

       
    #to make things easier we will only accept and read the 1st command being sent either be it for the small or large servo whichever comes 1st in the buffer:
    print("servo header array[0] is: %s \n" % servo_header)
    
    if (rxSm_flag == True):
        servo1_data = int(servo_header[servo1_headerFlag]) /10
        print("servo 1  data to write is: %f \n" % servo1_data)
      
        rxSm_flag = False

    if (rxLg_flag==True):
        servo2_data = int(servo_header[servo2_headerFlag]) /10
        print("servo 2  data to write is: %f \n" % servo2_data)
      
        
        rxLg_flag = False
    
    
    count = count+1
    #ser_rx._RadioSerialBuffer.reset_input_buffer()
    #ser_rx._RadioSerialBuffer.flushInput()#clear the buffer


  
   

      



   

    
ser_rx.close()
#cv2.destroyAllWindows()

