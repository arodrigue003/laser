import RPi.GPIO as GPIO
from time import time
import sys
import array
import warnings
warnings.filterwarnings("ignore")

# Variable globale

N = 0.005
horloge = 0.0001
resend_count = 3
message_length = 1


# Lancement du programme

if len(sys.argv) < 2:
  sys.exit('Usage: sudo %s file_name [resend_count] [message_length] [horloge]' % sys.argv[0])
if len(sys.argv) > 2:
  resend_count = int(sys.argv[2])
if len(sys.argv) > 3:
  message_length = int(sys.argv[3])
if len(sys.argv) > 4:
  horloge = float(sys.argv[4])
if len(sys.argv) > 5:
  N = float(sys.argv[5])
# Recuperation des bits du fichier

print 'Frequency : ' + str(horloge)
print 'Resend count : ' + str(resend_count)
print 'Payload length : ' + str(message_length)
print 'Break time : ' + str(N)

bytes_tab = []
def get_file_bytes(filename, bytes_tab):
  file = open(filename,'rb')
  try:
    byte = file.read(1)
    while byte != "":
      bytes_tab.append(byte)
      byte = file.read(1)
  finally:
    file.close()

get_file_bytes(sys.argv[1], bytes_tab)

def get_bits(byte):
  byte = ord(byte)
  for i in xrange(8):
    yield int((0b10000000 >> i) & byte > 0)

def int_to_bin(val, nb_max_bit):
  bin = format(val, 'b')
  bin = '0'*(nb_max_bit - len(bin))+bin
  return bin

def send_bit(bit):
  if int(bit) == 1:
    GPIO.output(12, GPIO.LOW)
    wasted(horloge/2)
    GPIO.output(12, GPIO.HIGH)
  elif int(bit) == 0:
    GPIO.output(12, GPIO.HIGH)
    wasted(horloge/2)
    GPIO.output(12, GPIO.LOW)
  wasted(horloge/2)
  

# =====================
# Transfert du fichier
# =====================

GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

# Attente active
# --------------

def wasted(smv):
  time0 = time()
  while (time() - time0 < smv):
    i = 1

# Sequence de synchronisation
# ----------------------------

def link_the_sync(horloge):
    sync = [1,1,1,1,1,1,1,1]
    for elmt in sync:
      send_bit(elmt)

      
# Transmission du fichier
# ------------------------

# 11111111 | Message1 | N ms | 11111111 | Message1 | N ms | 11111111 ......

# message_length: taille MAX des messages transmis

def send_byte(byte):
  for b in get_bits(byte):
    send_bit(b)

def send_trame(i, j):
  while (i < j):
    send_byte(bytes_tab[i])
    i += 1

def send_sequence_number(sequence_number):
    sequence_number_bin = int_to_bin(sequence_number,4)
    for i in sequence_number_bin:
      send_bit(i)

def send_data_size(data_size):
    data_size_bin = int_to_bin(data_size,6)
    for i in data_size_bin:
      send_bit(i)
      
def repeat_trame(i, j, sequence_number):
  for k in xrange(resend_count):
    link_the_sync(horloge)
    send_sequence_number(sequence_number)
    send_data_size(j-i)
    send_trame(i,j)
    wasted(N)
    
def send(N, horloge, resend_count, message_length):
  length_tab = len(bytes_tab)
  link_the_sync(horloge)
  wasted(N)
  for r in xrange(0, length_tab, message_length):
    repeat_trame(r, min(length_tab, r+message_length), ((r/message_length)+1)%16)
  wasted(0.1)


# !!! Penser a bien avoir N >> horloge !!!
# threshold minimal de 4*10^(-6) pour l'horloge

send(N, horloge, resend_count, message_length)

# =================
# Fin du programme
# =================
#print cpt/d

GPIO.cleanup()
