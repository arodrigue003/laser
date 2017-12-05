# -*- coding: utf-8 -*-

import serial
import time
import os, sys

bd = sys.argv[1]

print("Baudrate: " + bd)
# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial("/dev/ttyAMA0", bd, timeout=1.0)

#if (ser.isOpen() == False):
#    ser.open()
#    print('port open')


outStr = bytes(bytearray([i for i in range(0,256)]))


#bytes_sent = ser.write(open("tx.py", "rb").read())
#print(outStr)
bytes_sent = ser.write(outStr)
bytes_sent += ser.write('\n');
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
