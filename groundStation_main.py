import sys
# this is where python stores modules, yours could be different
#sys.path.append(r"D:/Alessandro/python39/Lib/site-packages")

sys.path.append(
    "C:/Users/MIMS-PC/AppData/Local/Programs/Python/Python39/Lib/site-packages")
sys.path.append(r"E:\school_teams\environment2\Lib\site-packages")
sys.path.append(r"D:\ALESSANDRO\MIMS lab-UAV project\Library-encoder-decoder\src")


import time
#import cv2
import serial
import rrc_decoder as d
import random 
import cv2 
import csv
import pandas as pd

#radio variables:
TX_PORT = 'COM4'
baud = 57600
gnd_station_connect = False
radio_type = "RFD" 

#servo variables:
header_servo1 = "Sm" #Small servo 
header_servo2 = "Lg" # Large servo 
servo1_flag = False
servo2_flag = False
servo_commands_2send = 0
servo_max_range = 12 # max %duty cycle of servo1
max_range = 360 #in degrees
test_img_path = r"D:\ALESSANDRO\MIMS lab-UAV project\Groundstation\images\tile.JPG"
read_data = 0
header = []
split_data=0
servo1_headerIndex =0
servo2_headerIndex = 0
servo1_dataIndex = 0
servo2_dataIndex = 0
# csv variables:
csv_path = r"D:\ALESSANDRO\MIMS lab-UAV project\Groundstation\datalog.csv"
csv_flag = True

fieldnames = ["header","value"]

####    initilization    ####
# radio init:
while True:

    port = TX_PORT
    baud = baud

    try:
        ser_gnd_station = d.radioConnection(port, baud)

        if(radio_type=="3DR"):
            ser_gnd_station._RadioSerialBuffer = serial.Serial(
                port=port,
                baudrate=baud,
                parity=serial.PARITY_EVEN,
                stopbits=serial.STOPBITS_TWO,
                bytesize=serial.EIGHTBITS,xonxoff=True,
                timeout=None)
            gnd_station_connect = True

        elif (radio_type == "RFD"):
            gnd_station_connect = True

        break
    except Exception as e:
        print(e)
        gnd_station = False
        exit(-1)

print(radio_type + " connected to: " + ser_gnd_station._RadioSerialBuffer.portstr )

# csv file init: 

with open(csv_path, 'w+') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
print("finished writing headers to csv file\n")
#============= MAIN LOOP:========================

while gnd_station_connect ==True:
    with open(csv_path,'a') as csv_file:
        img = cv2.imread(test_img_path)
        cv2.imshow('imageWindow',img)
        if(cv2.waitKey(1000) & 0xFF == ord('+')):
            servo_commands_2send = servo_commands_2send + 0.5
            print(servo_commands_2send)
        elif(cv2.waitKey(1000) & 0xFF == ord('-')):
            servo_commands_2send = servo_commands_2send - 0.5
            print(servo_commands_2send)
    

        if ((servo_commands_2send > max_range) or (servo_commands_2send < 0)):
            servo_commands_2send=0
            print("commands exceeded range. RESETTING VALUES \n")
        
        
        if(cv2.waitKey(2000) & 0xFF == ord('s')):
            servo1_flag = ser_gnd_station.sendCommand(header_servo1)
            if (servo1_flag == 1):
                servo1_com = int(10*servo_commands_2send)
                ser_gnd_station._RadioSerialBuffer.write(bytes(str(servo1_com),'utf-8'))
                ser_gnd_station._RadioSerialBuffer.write(b'\n')
            
                print("sent data success!\t header_servo1 sent was: %s%d \n" % (header_servo1,servo1_com))
                servo1_flag = False

        elif(cv2.waitKey(2000) & 0xFF == ord('l')):
            servo2_flag = ser_gnd_station.sendCommand(header_servo2)
            if (servo2_flag == 1):
                servo2_com = int(10*servo_commands_2send)
                ser_gnd_station._RadioSerialBuffer.write(bytes(str(servo2_com),'utf-8'))
                ser_gnd_station._RadioSerialBuffer.write(b'\n')
            
                print("sent data success!\t header_servo2 sent was: %s%d \n" % (header_servo2,servo2_com))
                servo2_flag = False
        else:
            print("idle: radio has not sent a command.\n")
            ser_gnd_station.sendCommand("idle")
        
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        data_read = ser_gnd_station.readString()
        if (data_read == None):
            data_read = "none\n"
            print("uav sent none type data \n")


        data_read_header = data_read.split('\n')
        if(len(data_read_header)>=2):
            for i in range(0,len(data_read_header)):
                header_test = data_read_header[i]
                if (header_test == '\x00'):
                    data_read_header.replace('\x00','')
                elif(header_test == header_servo1):
                    servo1_headerIndex = i
                    servo1_dataIndex = i+1
                elif(header_test == header_servo2):
                    servo2_headerIndex = i
                    servo2_dataIndex = i+1
            
                    #print("length of data read header: %d\n"%len(data_read_header))
                    #print("servo1_data index: %d\n" % servo1_dataIndex)
                    #print("servo2_data index: %d\n" % servo2_dataIndex)
                    info = {"header": data_read_header[servo1_headerIndex], "value":data_read_header[servo1_dataIndex]}
                    csv_writer.writerow(info)
                    info2 = {"header":data_read_header[servo2_headerIndex], "value":data_read_header[servo2_dataIndex]}
                    csv_writer.writerow(info2)

        
            
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            print("quitting now\n")
            break

#====== terminators: =====================  

csv_file.close()

ser_gnd_station._RadioSerialBuffer.close()
cv2.destroyAllWindows() # destroys image window 
sys.exit(0)

