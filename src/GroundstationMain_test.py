import sys
# this is where python stores modules, yours could be different
sys.path.append(r"D:/Alessandro/python39/Lib/site-packages")

import tty,termios

import time as t
import rrc_decoder as d
import serial

port = '/dev/ttyUSB0'
baud  = 57600 
####    initilization    ####
i =0 
count = 0
radio_connect = False
rx_command = False
rx_data_com = False
while True:

    try:
        radio = d.radioConnection(port, baud)
        radio_connect = True
        break
    except Exception as e:
        print(e)
        radio_connect = False
        exit(-1)

print("Connected")

filedescriptors = termios.tcgetattr(sys.stdin) # retrieves current terminal settings 
tty.setcbreak(sys.stdin) # allows for single character commands in terminal ; RAW mode instead of COOKED  mode
#tty and termios make sure terminal reads the key inputs 
while (radio_connect == True):
    
    #byteInWait = radio._RadioSerialBuffer.inWaiting()
    
    data_str= radio.readString()#_RadioSerialBuffer.read(byteInWait).strip().decode("utf-8")    # write a string
    print("data is %s \n" % data_str)
    #print("# bytes in wait: %d \n" % byteInWait)
    t.sleep(1)
      
    if (data_str == 'idle'):
        x=sys.stdin.read(1)[0]
        print("You pressed", x)
    
        if (x== "l"):
            radio.sendCommand("launch")
            print("sending launch command \n")
            t.sleep(0.5)
            rx_command = True
            rx_data_com = True
            break
    
    else:
        print("packet error\n")
    
    print("data command is: %s\n"% data_str) 

    t.sleep(1)
print("launch successfull\n")
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)

while(rx_command == True):
    packets = radio.getPackets()
    
    if packets == None:
        print("an error happend")
        continue
  
    result = d.decodePackets(packets)
    print(result)
    if result["corrupted"]:
        print("CORRUPT: " + str(i))
        continue

    result.pop("checksum")
    
    i=i+1
    t.sleep(1)
    
print("ERROR!")
radio.close()


