# -*- coding: utf-8 -*-

import sys, os
import serial
import time
import base64
import hashlib
from math import floor, ceil

def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def get_sleep_time(filesize):
    return 0
dirpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append( dirpath + "/../modules")
from baudrate import checkBaudrateHelp
if(len(sys.argv) < 2):
    checkBaudrateHelp("-h");
    exit(1)

bd = checkBaudrateHelp(sys.argv[1])

filename = dirpath + "/../../../test/default.txt"
if(len(sys.argv) < 3):
    print("Default file will be sent: " + filename)
else:
    filename = sys.argv[2]
    print("File " + filename + " will be sent")



# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial("/dev/ttyAMA0", bd, timeout=1.0)

# compute estimated time
sizeB = os.path.getsize(filename)
size = sizeB *8 
sizeB = ceil(sizeB / 3) * 4

string = ""
encoded = ""
Ubytes_sent = 0
Tbytes_sent = 0

fd = open(filename, "rb")

print("Expected transmission time: " + str((size/bd)*2) + "s")

start = time.time();

for chunk in read_in_chunks(fd,33333):
	encoded = base64.b64encode(chunk)
	string += encoded
	Ubytes_sent += ser.write(encoded)
        ser.write("\n")
        Tbytes_sent += 1
        # Uncomment followings lines to send the hash of each bloc, you need to also do it in rx.py
        #md5 = hashlib.md5(encoded).hexdigest()
        #ser.write(md5)
        #ser.write("\n")
        #Tbytes_sent += len(md5) + 1
        print(str(floor(100*Ubytes_sent/sizeB)) + "% ")
        if bd > 150000: #need a sleep for higher baud rates
            time.sleep(0.6)

# sending hash
ser.write("<\n")
md5 = hashlib.md5(string).hexdigest()
md5_len = ser.write(md5)
ser.write("\n")
Tbytes_sent += 2 + len(md5) + 1
Tbytes_sent += Ubytes_sent

end = time.time()
elapsed = end-start

# computing statistics of the file transfert
print("Total " + 
        str(Tbytes_sent) + " octets en " + str(elapsed) + " sec: "+
        str(Tbytes_sent/elapsed) + " o/s")

print("Utile: " + str(Tbytes_sent) + "/" + str(Ubytes_sent) + ": "+
        str(100*(Ubytes_sent/float(Tbytes_sent))) + "%. " +
        str(Ubytes_sent/elapsed) + " o/s")
print("md5: " + md5)

