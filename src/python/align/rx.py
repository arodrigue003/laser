import serial
import time
import base64

import os, sys

bd = sys.argv[1]

print("Baudrate: " + bd);

ser = serial.Serial("/dev/ttyAMA0", bd, timeout=1.0)

readline = lambda : iter(lambda:ser.read(1),"\n")
#with open("somefile.txt","wb") as outfile:
#    while True:
#        line = "".join(readline())
#        if line == "<<EOF>>":
#            break #done so stop accumulating lines
#        print >> outfile,line
        
while True:
    data = ser.readline()
    if data:
        string = str(data)
        print string
        #print string
        break;
    else:
        print "rien recu"
    #print string
