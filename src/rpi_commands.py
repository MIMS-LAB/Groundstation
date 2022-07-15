import sys

sys.path.append(
    "C:/Users/MIMS-PC/AppData/Local/Programs/Python/Python39/Lib/site-packages")

sys.path.append(r"E:\school_teams\environment2\Lib\site-packages")
import time
import serial
import cv2


radio =serial.Serial(
    port='COM13',\
    baudrate=57600,\
    parity=serial.PARITY_EVEN,\
    stopbits=serial.STOPBITS_TWO,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

commands2send = 0
max_range = 12 # max %duty cycle of servo1
test_img_path = r"D:\ALESSANDRO\MIMS lab-UAV project\Groundstation\images\test_img1.jpg"
read_data = 0
header = []
split_data=0

while(True):
    
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
        radio.write(pc_header)
        radio.write(int (10*commands2send))
        radio.write(b'\n')
        print("sending values:\t")
        print(commands2send)
      
    if cv2.waitKey(0) & 0xFF == ord('q'):
        print("quitting now\n")
        break

radio.close()
cv2.destroyAllWindows()         # closes the windows opened by cv2.imshow()
sys.exit()