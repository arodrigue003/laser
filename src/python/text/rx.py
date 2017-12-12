import serial
import time
import os, sys

bd = sys.argv[1]
nb = int(sys.argv[2])
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

sentString = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean varius leo dignissim sapien ultricies viverra sit amet sed libero. Quisque ac neque nec tortor ultricies malesuada. Donec ipsum odio, volutpat non blandit vel, dapibus eu mauris. Praesent dapibus ultricies blandit. Nullam auctor faucibus nulla, sollicitudin eleifend justo tempus non. Vestibulum non congue purus. Proin interdum malesuada neque sit amet porttitor. Pellentesque et lectus a elit venenatis tincidunt. Curabitur non purus finibus, fringilla nisl id, fermentum elit. Nulla ac ipsum justo. Integer sodales rutrum mauris eu viverra. In aliquam nulla et enim tempor dignissim. Etiam a imperdiet nisl, quis porta orci. Nam tincidunt luctus elit at iaculis. Nunc consectetur velit lorem, a congue nulla lacinia id. Cras et sem eros. '

crap = 0

for i in range(0, nb-1):
    sentString += sentString

while True:
    data = ser.readline()
    if data[:-1] == "<<EOF>>":
        break
    if data:
        print data[:-1]
        sys.stdout.flush()
        if sentString == data[:-1]:
            print "\nOK"
        else:
            print "\nERROR"
            buf = ""
            for i in range(0, len(data)-1):
                if sentString[i] == data[i]:
                    buf += sentString[i]
                else:
                    if crap == 0:
                        crap = i
                    buf += ">" + sentString[i] + "|" + data[i] + "<"
                if( i % 20 == 0):
                    print buf
                    buf = ""
                    
        if crap != 0:
            print "ERROR AT " + str(crap)
        print "RECU " + str(len(data)-1) + " octets"
#        print len(data[:-1])
        #string+= str(data)
    #print string

#file = open("a.out", "wb")
#file.write(string)
#file.close()
