import sys, os
import serial
import time
import base64
import hashlib

sys.path.append(os.path.dirname(os.path.realpath(__file__)) +"/../modules")
from baudrate import checkBaudrateHelp
if(len(sys.argv) < 2):
    checkBaudrateHelp("-h");
    exit(1)

bd = checkBaudrateHelp(sys.argv[1])

ser = serial.Serial("/dev/ttyAMA0", baudrate=bd, timeout=1.0)

data = ""
md5 = ""

state = 0; # 0: waiting for data. 1: waiting for md5

while True:
    rcvd = ser.readline()
    if rcvd:
        if(state == 0):
            data = base64.b64decode(str(rcvd))
        elif(state == 1):
            md5 = str(rcvd)
            print("Checking md5...")
            print("rcved: ", md5)
            mmd5 = hashlib.md5(data).hexdigest()
            print("cmptd: ", mmd5)
            if(mmd5 == md5):
                print("ok! Enter file name or press enter to cancel:")
                filename = sys.stdin.readline();
                if(filename == ""):
                    print("cancelled")
                else:
                    file = open(filename, "wb")
                    file.write(data)
                    file.close()
            
        state = (state+1)%2
    else:
        print "waiting."

