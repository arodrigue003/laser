# -*- coding: utf-8 -*-

import serial
import time
import os, sys

bd = sys.argv[1]
nb = int(sys.argv[2])

#print(bd)
# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial("/dev/ttyAMA0", bd, timeout=1.0)#, bytesize=serial.SIXBITS)

#if (ser.isOpen() == False):
#    ser.open()
#    print('port open')

outStr ='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean varius leo dignissim sapien ultricies viverra sit amet sed libero. Quisque ac neque nec tortor ultricies malesuada. Donec ipsum odio, volutpat non blandit vel, dapibus eu mauris. Praesent dapibus ultricies blandit. Nullam auctor faucibus nulla, sollicitudin eleifend justo tempus non. Vestibulum non congue purus. Proin interdum malesuada neque sit amet porttitor. Pellentesque et lectus a elit venenatis tincidunt. Curabitur non purus finibus, fringilla nisl id, fermentum elit. Nulla ac ipsum justo. Integer sodales rutrum mauris eu viverra. In aliquam nulla et enim tempor dignissim. Etiam a imperdiet nisl, quis porta orci. Nam tincidunt luctus elit at iaculis. Nunc consectetur velit lorem, a congue nulla lacinia id. Cras et sem eros. '

#bytes_sent = ser.write(open("tx.py", "rb").read())

for i in range(0, nb-1):
    outStr += outStr

print(outStr)
bytes_sent = ser.write(outStr)
ser.write("\n<<EOF>>\n")

print "Envoyé ", bytes_sent, " octets (sans le breakline) => " + str(len(outStr))

ser.flushInput()

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

