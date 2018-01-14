import serial
import time
import base64

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) +"/../modules")
from baudrate import checkBaudrateHelp
if(len(sys.argv) < 2):
    checkBaudrateHelp("-h");
    exit(1)

bd = checkBaudrateHelp(sys.argv[1])
if(bd == -1):
    exit(0)

print("Baudrate: " + str(bd));

ser = serial.Serial("/dev/ttyAMA0", bd, timeout=1.0)

readline = lambda : iter(lambda:ser.read(1),"\n")
#with open("somefile.txt","wb") as outfile:
#    while True:
#        line = "".join(readline())
#        if line == "<<EOF>>":
#            break #done so stop accumulating lines
#        print >> outfile,line
        
verite = bytes(bytearray([i for i in range(55,256)]))

while True:
    data = ser.readline()
    if data:
        if data[0] == '\n':
            continue
        #string = str(data)

        array = []
        for i in range(0,200):
            try:
                #print("lul")
                array.append(data[i])
                #print("ok");
            except:
                break;
        

        ok = 0;
        for i in range(0,len(array)):
            if(verite[i] == array[i]):
                ok+=1;

        #print array
        print( str(ok) + " : " + str(len(array)) + "/" + str(len(verite)))
        sys.stdout.flush()
        #print string
        #print string
        #break;
    else:
        print "rien recu"
    #print string
