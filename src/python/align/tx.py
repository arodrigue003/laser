# -*- coding: utf-8 -*-

import serial
import time
import os, sys

sys.path.append("../modules")
from baudrate import checkBaudrateHelp
bd = checkBaudrateHelp(sys.argv[1])
if(bd == -1):
    exit(0)

print("Baudrate: " + bd)
# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial("/dev/ttyAMA0", bd, timeout=1.0)

#if (ser.isOpen() == False):
#    ser.open()
#    print('port open')


outStr = bytes(bytearray([i for i in range(55,256)]))


#bytes_sent = ser.write(open("tx.py", "rb").read())
#print(outStr)
while(True):
    bytes_sent = ser.write(outStr)
    for i in range(0,10):
        bytes_sent += ser.write('\n');
        time.sleep(0.01)
    time.sleep(1)
    print("sent")
#ser.write("\n<<EOF>>\n")
#print "Envoyé ", bytes_sent, " octets"

    #ser.flushInput()

    #for i,c in enumerate(outStr):
    #    print("send: " + outStr[0:i])
    #    ser.write((outStr[0:i]+"\n"))
    #    time.sleep(0.1)
        #inStr = ser.read(ser.inWaiting())

        #print ("inStr =  " + inStr.decode('UTF-8'))
        #print ("outStr = " + outStr)
        #if(inStr.decode('UTF-8') == outStr):
        #print ("WORKED")
        #else:
        #print ("failed")
   #     ser.close()
