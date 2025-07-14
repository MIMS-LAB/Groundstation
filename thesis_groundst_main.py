import sys

sys.path.append(r"D:\alessandro\Thesis\Onboard-Firmware\include\rrc_encoder\src")
sys.path.append(r"C:\Users\RUMIM\AppData\Roaming\Python\Python312\site-packages")

import pygame
import serial 
import rrc_decoder as d
import time as t

rxport= "COM7"
baud  = 9600
# This dict can be left as-is, since pygame will generate a
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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    data= rx_ser.readString()
    button = joystick.get_button(0)    
  
    if (button):
        axis = joystick.get_axis(0)
        print("axis:")
        print(axis)
        rx_ser.sendCommand("X" + str(axis) )
        print("sending X axis command \n")
    elif data == None:
        t.sleep(1)

        print("none type error")
        continue
    else:
        print(data)
        #data_str= data.split(',')

    


    
rx_ser._RadioSerialBuffer.close()
pygame.quit()
