import serial
import time
import os, sys

bd = sys.argv[1]
#print(bd)
ser = serial.Serial("/dev/ttyAMA0", baudrate=bd, timeout=1.0)#, bytesize=serial.SIXBITS)

#readline = lambda : iter(lambda:ser.read(1),"\n")
#with open("somefile.txt","wb") as outfile:
#    while True:
#        line = "".join(readline())
#        if line == "<<EOF>>":
#            break #done so stop accumulating lines
#        print >> outfile,line
        
string = ""
while True:
    data = ser.readline()
    if data[:-1] == "<<EOF>>":
        break
    if data:
        print data[:-1]
        sys.stdout.flush()
#        print len(data[:-1])
        #string+= str(data)
    #print string

#file = open("a.out", "wb")
#file.write(string)
#file.close()
