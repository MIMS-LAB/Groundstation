import sys

sys.path.append(r"D:\alessandro\Thesis\Onboard-Firmware\include\rrc_encoder\src")
sys.path.append(r"C:\Users\RUMIM\AppData\Roaming\Python\Python312\site-packages")

import pygame
import serial 
import rrc_decoder as d
import time as t
import cv2

rxport= "COM7"
baud  = 9600 #230400

# This dict can be left as-is, since pygame will generate 
# pygame.JOYDEVICEADDED event for every joystick connected
# at the start of the program.


joysticks = {}
while True:

    try:
        rx_ser =  d.radioConnection(rxport, baud)
      

        break
    except Exception as e:
        print(e)
        exit(-1)

print("Connected")
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Joystick Test")
running = True
button_state = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    data= rx_ser.readString()
    button = joystick.get_button(0)
    if button_state==False:
        if (button):  
            button_state = True
            axisX = round(joystick.get_axis(0),6)
            axisY = round(joystick.get_axis(1),6)
            throttle = -round(joystick.get_axis(3),6)

            rx_ser.sendCommand("\nT" + str(throttle) +"\nX" + str(axisX) +"\nY" + str(axisY) )
            print(" T:\t"+ str(throttle) +"\nX:\t" + str(axisX) +"\nY:\t" + str(axisY))
    if data == None:
        t.sleep(0.5)
        # print("none type error")
        continue
    else:
        print(data)
  
        button_state = False
            #data_str= data.split(',')



rx_ser._RadioSerialBuffer.close()
pygame.quit()
