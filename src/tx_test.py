'''
This file relates to sending header_servo1s to flight contorller to control servos via pc and not frsky taranis controller

'''

import sys
# this is where python stores modules, yours could be different
#sys.path.append(r"D:/Alessandro/python39/Lib/site-packages")

sys.path.append(
    "C:/Users/MIMS-PC/AppData/Local/Programs/Python/Python39/Lib/site-packages")
sys.path.append(r"E:\school_teams\environment2\Lib\site-packages")

import time
#import cv2
import serial
import rrc_decoder as d
import random 
import cv2 
TX_PORT = 'COM4'
baud = 57600
tx_connect = False


header_servo1 = "Sm" #Small servo 
header_servo2 = "Lg" # Large servo 
servo1_flag = False
servo2_flag = False

commands2send = 0
max_range = 12 # max %duty cycle of servo1
test_img_path = r"D:\ALESSANDRO\MIMS lab-UAV project\Groundstation\images\tile.JPG"
read_data = 0
header = []
split_data=0

####    initilization    ####

while True:

    port = TX_PORT
    baud = baud

    try:
        '''
        ser_tx = serial.Serial(
            port=port,
            baudrate=baud,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.EIGHTBITS,xonxoff=True,
            timeout=None)
        '''
        ser_tx = d.radioConnection(port, baud)
        tx_connect = True

        break
    except Exception as e:
        print(e)
        tx_connect = False
        exit(-1)

print(" connected to: " + ser_tx._RadioSerialBuffer.portstr)



while tx_connect ==True:
    img = cv2.imread(test_img_path)
    cv2.imshow('imageWindow',img)
    if(cv2.waitKey(0) & 0xFF == ord('+')):
        commands2send = commands2send + 0.5
        print(commands2send)
    elif(cv2.waitKey(0) & 0xFF == ord('-')):
        commands2send = commands2send - 0.5
        print(commands2send)

    if (commands2send > max_range):
        commands2send=0
        print("commands exceeded range. RESETTING VALUES \n")

   
    
     
    if(cv2.waitKey(0) & 0xFF == ord('s')):
        servo1_flag = ser_tx.sendCommand(header_servo1)
        if (servo1_flag == 1):
            servo1_com = int(10*commands2send)
            ser_tx._RadioSerialBuffer.write(bytes(str(servo1_com),'utf-8'))
            ser_tx._RadioSerialBuffer.write(b'\n')
        
            print("sent data success!\t header_servo1 sent was: %s%d \n" % (header_servo1,servo1_com))
            servo1_flag = False

        else:
            print("write buffer is still non empty")
            ser_tx._RadioSerialBuffer.flushOutput()
    if(cv2.waitKey(0) & 0xFF == ord('l')):
        servo2_flag = ser_tx.sendCommand(header_servo2)
        if (servo2_flag == 1):
            servo2_com = int(10*commands2send)
            ser_tx._RadioSerialBuffer.write(bytes(str(servo2_com),'utf-8'))
            ser_tx._RadioSerialBuffer.write(b'\n')
        
            print("sent data success!\t header_servo2 sent was: %s%d \n" % (header_servo2,servo2_com))
            servo2_flag = False

        else:
            print("write buffer is still non empty")
            ser_tx._RadioSerialBuffer.flushOutput()
        
    if cv2.waitKey(0) & 0xFF == ord('q'):
        print("quitting now\n")
        break

  
    
    #time.sleep(5)
    
    
    #ser_tx._RadioSerialBuffer.flushOutput()
    #time.sleep(5)

    
ser_tx._RadioSerialBuffer.close()
cv2.destroyAllWindows() # destroys image window 
sys.exit(0)

