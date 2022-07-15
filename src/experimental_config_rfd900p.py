

# -----------------------libraries:------------------------------

import sys
# this is where python stores modules, yours could be different
sys.path.append(r"D:/Alessandro/python39/Lib/site-packages")

import rrc_decoder as d
import os
import random
import time 

#import keyboard

from serial.serialutil import SerialException
import serial

#from SiKset import check_OK, command_mode

global baud,port  


baud = 57600

port = "COM4"           

#------------------------------------------------------------------


class radioConfig:

    current_version = "v1.0.2"  # changelog in repo

    # constants


    # *************** default values **********************


    DEFAULT_TX_PWR = 20  # in dB

    DEFAULT_NUM_CHANNELS = 1



    

    def __init__(self,ser):
        self.command_prefix = "AT"
       
        # ************* RANGES: ****************************


        self.serial_speeds = (2400,4800,9600,19200,38400,57600,115200) #structure==> {2400: 2, 4800: 4, 9600: 9,19200: 19, 38400: 38, 57600: 57, 115200: 115}

        self.air_speeds = (4, 8, 16, 24, 32, 64, 96, 128, 192, 250)

        self.netids = range(0,500)

        self.txpowers = range(1, 31)

        self.numb_channels = range(1, 50)

        self.ECCrange = (0,1)

        self.MAVLINKrange = (0,1)

        self.OP_RESEND_RANGE = (0,1)

        self.MIN_FREQ  = range(902000,928000,1000) # in kHz

        self.MAX_FREQ  = range(903000,929000,1000) # in kHz

        self.DUTY_CYCLE_RANGE = range(10,100)


        self.LBT_RSSI_range = (0,1)

        self.MANCHESTER_range = (0,1)

        self.rtscts_RANGE = (0,1)

        self.nodeID_range = range(0,30)

        self.NODEDESTINATION_range = range(0,30)

        self.SYNCANY_range = (0,1)

        self.NODECOUNT_range = range(2,31)


        self.RANGES = {self.serial_speeds, self.air_speeds, self.netids,self.txpowers,self.ECCrange,self.MAVLINKrange,self.OP_RESEND_RANGE,self.MIN_FREQ,self.MAX_FREQ,self.numb_channels,self.DUTY_CYCLE_RANGE,self.LBT_RSSI_range

        ,self.MANCHESTER_range,self.rtscts_RANGE,self.nodeID_range,self.NODEDESTINATION_range,self.SYNCANY_range,self.NODECOUNT_range}

        self.ser = ser

        self.ser.timeout = 0

        print("Serial port is {}".format(ser.port))

        self.command_prefix = "AT"

        self.ser.baudrate = baud


        #initially make sure that baud rate is in range:
    def INITIALIZE2(self,ser):
        if baud in self.serial_speeds:

            self.baud = baud

        else:

            print(baud, " baud is not a valid speed.")
            self.ser.close()


        print("Serial port speed set to", self.baud, "baud.")

        print("Serial port settings:\n\t", self.ser)


        # open the serial port

        try:
            self.ser.open()

        except SerialException:

            print("Couldn't open serial port {}".format(ser.port))
        

        print("Serial port {} opened.".format(ser.portstr))


        # enter command mode

        if not self.command_mode():

            print("Couldn't enter command mode")

            print("Check the port and the baudrate")

            return 1

        # flush the input and output buffers

        self.ser.flushOutput()

        self.ser.flushInput()

        time.sleep(1)           # give the flush a second. //Reason for this?

        return 0


    def check_OK(self,response):

        """Checks for an "OK" response within a string."""

        ok = "OK" in response

        if not ok:

            print("ERROR: OK not found in response")

        return ok



    def get_response(self):

        """Gets a response from the serial port."""

        sleep_time_after_buffer_read = 2

        # vprint("Characters in receive buffer before reading:", inBuffer)

        response = b''

        while self.ser.inWaiting():

            # vprint("Reading serial port buffer.")

            self.response += ser.readline()

            # vprint("Response:", response.decode('utf-8', errors='ignore'))

            time.sleep(sleep_time_after_buffer_read)

            # vprint("Characters in receive buffer after reading and waiting %d seconds:" % sleep_time_after_buffer_read, ser.inWaiting())

        print("No more characters in serial port buffer.")

        return response.decode('utf-8', errors='ignore')



    def command_mode(self):

        """Enters command mode"""

        self.ser.flushOutput()

        self.ser.flushInput()

        time.sleep(1)           # give the flush a second

        self.ser.write(b'\r\n')  # the ATO command must start on a newline

        print("Sent newline and carriage return")

        time.sleep(0.5)

        command = "ATO\r\n"     # exit AT command mode if we are in it

        self.ser.write(command.encode('utf-8'))

        print("Sent command: '{}'".format(command.strip()))

        time.sleep(1)

        # test to see if we are stuck in AT command mode.  If so, we see a response from this.

        command = "ATI\r\n"

        print("Sent command: '{}'".format(command.strip()))

        time.sleep(1.5)           # minimum 1 second wait needed before +++

        command = "+++"         # +++ enters AT command mode

        ser.write(command.encode('utf-8'))

        print("Sent command: '{}'".format(command.strip()))

        time.sleep(2)           # minimum 1 second wait after +++

        response = self.get_response()

        if self.check_OK(response):

            return True

        else:

            return False


    # Notes about serial port modes:

    # when opening the serial port,

    # possible timeout values:

    #    1. None: wait forever, block call

    #    2. 0: non-blocking mode, return immediately

    #    3. x, x is bigger than 0, float allowed, timeout block call


   

    


    def process_user_input(selectedParam,paramValue):

        Strings = {"SERIAL_SPEED","AIR_SPEED","NET_ID","TX_PWR","ECC","MAVLINK"

        , "OPPRESEND","MIN_FREQ","MAX_FREQ","NUM_CHANNELS","DUTY_CYCLE","LBT_RSSI"

        ,"MANCHESTER","RTSCTS","NODEID","NODEDESTINATION","SYNCANY","NODECOUNT"}


        for i in range(0,19): 

            testHeader = "S" + str(i)


            if (selectedParam==testHeader):

                parametersString = Strings[i]

                testValue = RANGES[i]
            

                if(paramValue in testValue):

                    any_change = True

                

                else:

                    print("Invalid input.")

                    return 1
                

        if (any_change==True):

            if ((selectedParam == "S1") or (selectedParam == "S2") or (selectedParam == "S3") or (selectedParam == "S4") or (selectedParam=="S8") or (selectedParam=="S9") or (selectedParam=="S10")):

                print("changing %s to %d: \n" % (parametersString,int(paramValue)))

                command = "%s%s=%d\r\n" % (command_prefix,selectedParam,int(paramValue))


                print("Sending command: {}".format(command.strip()))

                ser.write(command.encode('utf-8'))

                time.sleep(2)

                response = get_response()

                if not check_OK(response):

                    print("Setting failed. Exiting.")
                    ser.close()
            
            

        return 0


    def rfdConfig_main(ser):

        ######

        # DO ALL THESE THINGS

        ######

        #  0. show parameters

        #  1. set SERIAL_SPEED

        #  2. set AIR_SPEED

        #  3. set NET_ID

        #  4. set TXPOWER

        #  5. set ECC

        #  6. set MAVLINK

        #  7. set OPPRESEND

        #  8. set MIN_FREQ

        #  9. set MAX_FREQ

        # 10. set NUM_CHANNELS

        # 11. set DUTY_CYCLE

        # 12. set LBT_RSSI

        # 13. set MANCHESTER

        # 14. set RTSCTS

        # 15. set NODEID

        # 16. set NODEDESTINATION

        # 17. set SYNCANY

        # 18. set NODECOUNT


        ######

        # 0. show parameters

        ######

        print("Getting parameters.")

        command = "%sI5\r\n" % command_prefix

        print("Sending command: {}".format(command.strip()))

        ser.write(command.encode('utf-8'))

        time.sleep(2)

        response = get_response()
        print(response)
        ser.close()



        any_change = False

        print("select a parameter from S1-S18:")

        selectedParam = input()

        print("now select a value: \n")

        paramValue  = input()
        

        process_user_input(selectedParam, paramValue)

        # write to EEPROM and reboot

        if any_change:

            command = "%s&W\r\n" % command_prefix

            print("Sending command: {}".format(command.strip()))

            ser.write(command.encode('utf-8'))

            time.sleep(2)

            response = get_response()

            if not check_OK(response):

                print("ERROR writing parameters in EEPROM")

            command = "%sZ\r\n" % command_prefix

            print("Sending command: {}".format(command.strip()))

            ser.write(command.encode('utf-8'))


        # close the serial port
        ser.close()

        print("Serial port {} closed.".format(ser.portstr))




        return 0 


def key_pressed(key):

    if (keyboard.is_pressed(key)):

        print(key + " is pressed")

        return 0

    else:

        return 1



def rfdKey_events():

    if(key_pressed('s') == 0):

        radio.sendCommand("launch")

        print("sending launch command. \n")

        return 0
    

    if(key_pressed('r') == 0):

        print("changing rfd settings \n")

        return 0 


    return 1     



if __name__ == "__main__":
    

    count = 0
    radio = d.radioConnection(port,baud)

    while count < 300:

        if(rfdKey_events()==0):

            ser = radio._RadioSerialBuffer

            radioCONFIG = radioConfig(ser)

            if(radioCONFIG.INITIALIZE2(ser)==0):
                radioCONFIG.rfdConfig_main(ser)
        
        print(count)

        count = count+1

        time.sleep(1)

