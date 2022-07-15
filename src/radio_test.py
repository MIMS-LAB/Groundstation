'''
This file relates to sending commands to flight contorller to control servos via pc and not frsky taranis controller

'''

import sys
# this is where python stores modules, yours could be different
sys.path.append(
    r"C:\Users\MIMS-PC\AppData\Local\Programs\Python\Python39\Lib\site-packages")
sys.path.append(r"E:\school_teams\environment2\Lib\site-packages")

import time
import cv2
import serial
RX_PORT = 'COM13'
TX_PORT = 'COM4'
baud = 57600
response = b''  
waiting  = 0
####    initilization    ####

while True:

    port = TX_PORT
    baud = baud

    try:
        ser_tx = serial.Serial(
            port=port,
            baudrate=baud,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.EIGHTBITS,xonxoff=True,
            timeout=None)
        break
    except Exception as e:
        print(e)
        exit(-1)

print(" connected to: " + ser_tx.portstr)

while True:

    port = RX_PORT
    baud = baud

    try:
        ser_rx = serial.Serial(
            port=port,
            baudrate=baud,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.EIGHTBITS,xonxoff=True,
            timeout=None)
        break
    except Exception as f:
        print(f)
        exit(-2)
print(" connected to: " + ser_rx.portstr)


# with ser as ser:
'''
ser.close()
ser.open()
'''

while True:
    
    #ser_rx.flushInput()
    ser_tx.flushOutput()
    time.sleep(1)

    sent_data = ser_tx.write(b"start\n")
    print("sent data is: %s \n" % sent_data)

    #data = ser.inWaiting()
    '''
    while ser_rx.inWaiting():
        print("Reading serial port buffer.")
        response += ser_rx.readline()
        print("Response:", response.decode('utf-8', errors='ignore'))
        time.sleep(sleep_time_after_buffer_read)
        print("Characters in receive buffer after reading and waiting %d seconds:" % sleep_time_after_buffer_read, ser.inWaiting())
        print("No more characters in serial port buffer.")
        response.decode('utf-8', errors='ignore') # so response is a string==> ie- serial.read returns strings 
    
    '''

    waiting = ser_rx.inWaiting()

    time.sleep(1)

    response = ser_rx.read(waiting).strip().decode("utf-8")
    
    print("in waiting data is: %s \n" % waiting)
    
    print("******* read data is:%s ********\n " % response)
    
    '''
    if (data !=""):
        string_array += ser.read(data).strip().decode('utf-8')
        print(string_array)
        time.sleep(1)
    else:
        print("no data read")     
        time.sleep(1)
    '''
    if (cv2.waitKey(0) & 0xFF == ord("q")):
        print("closing windows and ser comms")

        break
ser.close()
cv2.destroyAllWindows()

