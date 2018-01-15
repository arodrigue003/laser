import sys, os
import serial
import time
import base64
import hashlib
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) +"/../python/modules")
from baudrate import checkBaudrateHelp
if(len(sys.argv) < 2):
    checkBaudrateHelp("-h");
    exit(1)

#bd = checkBaudrateHelp(sys.argv[1])
os.system("rm out")
os.system("./rx "+sys.argv[1]+" /dev/ttyAMA0")

ser = open('out', 'r')
#ser = serial.Serial("/dev/ttyAMA0", baudrate=bd, timeout=1.0)

data = ""
md5 = ""

state = 0; # 0: waiting for data. 1: waiting for md5

while True:
    rcvd = ser.readline()
    if rcvd:
        print("en cours de reception...")
        if(state == 0):
            if(rcvd[0] == "<"):
                print("waiting for md5...")
                state = 1
                continue
            data += rcvd[0:-1] # Should be faster
            #data += rcvd.rstrip()
            ##############
            #md5 = ser.readline()[0:-1]
            #mmd5 = hashlib.md5(rcvd[0:-1]).hexdigest()
            #if(md5 == mmd5):
            #    print("-- ok "+ md5)
            #else:
            #    print("ERROR")
            #    print(" md5:" + md5)
            #    print("mmd5:" + mmd5)
            #############
        elif(state == 1):
            md5 = rcvd.rstrip()
            print("Checking md5...")
            mmd5 = hashlib.md5(data).hexdigest()
            if(mmd5 == md5):
                print("ok! Enter file name or press enter to cancel:")
                filename = sys.stdin.readline().rstrip();
                if(filename == ""):
                    print("cancelled")
                else:
                    data = base64.b64decode(data)
                    file = open(filename, "wb")
                    file.write(data)
                    file.close()
                    print("Data written in file " + filename)
            else:
                print("!! ERROR in md5. Try to realign the lasers")
                print("md5 recieved: " + md5)
                print("md5 computed: " + mmd5)
            state = 0
            data = ""
    else:
        break
        print "."

