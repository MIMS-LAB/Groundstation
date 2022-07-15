import serial 
import time as t

Port = '/dev/ttyUSB0'
Baud  = 57600

ser = serial.Serial(port = Port, baudrate = Baud)  # open first serial port
dataInWait = data= ""
while True:
    ser.flushOutput()
    ser.flushInput()
    
    dataInWait = ser.inWaiting()
    data= ser.read(dataInWait).strip().decode("utf-8")    # write a string
    print(data)
    
ser.close()             # close port