import serial
import time
import base64

ser = serial.Serial("/dev/ttyAMA0", baudrate=110, timeout=1.0)

        
while(1):
    ser.write("a")
    time.sleep(0.5)

ser.close();
