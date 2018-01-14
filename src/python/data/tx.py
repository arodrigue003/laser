# -*- coding: utf-8 -*-

import sys, os
import serial
import time
import base64
import hashlib

dirpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append( dirpath + "/../modules")
from baudrate import checkBaudrateHelp
if(len(sys.argv) < 2):
    checkBaudrateHelp("-h");
    exit(1)

bd = checkBaudrateHelp(sys.argv[1])

filename = dirpath + "/default.txt"
if(len(sys.argv) < 3):
    print("Default file will be sent: ", filename)
else:
    filename = argv[2]
    print("File ", filename, " will be sent")



# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial("/dev/ttyAMA0", bd, timeout=1.0)

string = open(filename, "rb").read()
md5 = hashlib.md5(string).hexdigest()

start = time.time();

bytes_sent = ser.write(string)
ser.write("\n")
md5_len = ser.write(md5)
ser.write("\n")

end = time.time();

print("Envoyé ", bytes_sent, " + ", md5_len, " octets en ", (end - start), " sec")
print("md5: ", md5)

