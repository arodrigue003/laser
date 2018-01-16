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

# get the baud rate from the input argument
bd = checkBaudrateHelp(sys.argv[1])

# open serial port
ser = serial.Serial("/dev/ttyAMA0", baudrate=bd, timeout=1.0)

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
            data += rcvd[0:-1]
            # Uncomment followings lines to check the hash of each bloc, you need to also do it in tx.py
            #md5 = ser.readline()[0:-1]
            #mmd5 = hashlib.md5(rcvd[0:-1]).hexdigest()
            #if(md5 == mmd5):
            #    print("-- ok "+ md5)
            #else:
            #    print("ERROR")
            #    print(" md5:" + md5)
            #    print("mmd5:" + mmd5)
        elif(state == 1):
            md5 = rcvd.rstrip() # received md5
            print("Checking md5...")
            mmd5 = hashlib.md5(data).hexdigest() # computed md5
            # check if the computed md5 is equal to the received one or not
            if(mmd5 == md5):
                # saving procedure with data decoding
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
                # showing difference between hashs
                print("!! ERROR in md5. Try to realign the lasers")
                print("md5 recieved: " + md5)
                print("md5 computed: " + mmd5)
            state = 0
            data = ""
    else:
        # display that the script is still able to receive data
        print "."

