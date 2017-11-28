import serial
import time
import base64

ser = serial.Serial("/dev/ttyAMA0", baudrate=230400, timeout=1.0)

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
    #if data[:-1] == "<<EOF>>":
        #break
    if data:
        #print data[:-1]
        string = str(data)
        print string
        string = base64.b64decode(string)
        #print string
        break;
    else:
        print "rien recu"
    #print string

file = open("a.out", "wb")
file.write(string)
file.close()
