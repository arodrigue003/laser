import RPi.GPIO as GPIO
import time
import sys
import array
import math
import numpy as np
import warnings
warnings.filterwarnings("ignore")


def binaries_to_bytes(bi):
  s = ''.join(str(x) for x in bi)
  return [ s[i:i+8] for i in range(0, len(s), 8) ]

def save_binary(data):
  file = open("output.txt",'wb')
  for byte in data:
    n = int(byte, 2)
    d = chr(n)
    file.write(d)
  file.close()


class Receptor:

  def __init__(self, size_pl = 8, time_inter_trame = 5, duplicata = 3):    
    self.log_t = []
    self.log_s = []
    self.log_nt = []
    self.log_b = 0
    self.freq = 0
    self.msg_data = []
    self.msg_t = []
    self.msg_beg = 0
    self.beg = 0
    self.log = True

    self.size_pl = size_pl
    self.time_inter_trame = time_inter_trame
    self.duplicata = duplicata
    self.msg = []

    self.size = 0
    self.packets = {}
    self.packet_number = 0
    self.old_packet_number = 0
    self.old_sequence_number = 0
    self.older_sequence_number = 0
    self.sequence_number = 0
    self.data_size = 0
    self.max_seq_num = 15
    self.max_data_size = 0

    # Configuration du recepteur
    # ---------------------------

    GPIO.cleanup()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.IN)
    GPIO.add_event_detect(11, GPIO.RISING)
    GPIO.setup(12, GPIO.IN)
    GPIO.add_event_detect(12, GPIO.FALLING)

  def rcv_bit(self, bit, ti):
    self.msg_data.append(bit)
    self.msg_t.append(ti - self.msg_beg)
    
  def log_rise(self, ti):
    t = ti - self.log_b;
    self.log_t.append(t-0.00000001)
    self.log_s.append(-1)
    self.log_t.append(t)
    self.log_s.append(1)


  def log_fall(self, ti):
    t = ti - self.log_b;
    self.log_t.append(t-0.00000001)
    self.log_s.append(1)
    self.log_t.append(t)
    self.log_s.append(-1)

  def log_next(self):
    self.log_nt.append(time.time() - self.log_b + (self.freq * 0.75))

  def save_log(self):
    file = open("log.txt",'w')
    file.write("Time;State;Val\n")
  
    size = len(self.log_nt)
    j = 0
    state = 0
    for i in xrange(len(self.log_t)):

      if j < size and self.log_nt[j] < self.log_t[i]:
        file.write(str(self.log_nt[j]-0.000001)+";"+str(state)+";0\n")
        file.write(str(self.log_nt[j]-0.0000001)+";"+str(state)+";-0.5\n")
        file.write(str(self.log_nt[j]+0.0000001)+";"+str(state)+";0.5\n")
        file.write(str(self.log_nt[j]+0.000001)+";"+str(state)+";0\n")
        j = j + 1

      line = str(self.log_t[i])+";"+str(self.log_s[i])+";0"
      state = self.log_s[i]
      file.write(line+"\n")
    file.close()

  def sync(self):
    
    a = 0
    while not GPIO.event_detected(11): # rise
      a = 0

    # Synchronisation
    # -------%------------------------------------

    # Phase 1 : Reception de cinq 1
    freqs = []
    self.beg = time.time()
    save_beg = time.time()
    self.log_b = time.time()
    cpt = 7
    while cpt:
      if GPIO.event_detected(11): # Rise
        self.log_rise(time.time())
        cpt = cpt - 1
        a = time.time()
        freqs.append(a-save_beg)
        save_beg = a
      elif GPIO.event_detected(12): # Fall
        self.log_fall(time.time())
    self.freq = freqs[3]

  def download(self):
    
    # Download msg
    # ---------------------------------------
    self.msg_beg = time.time()
    self.log_next()
    while time.time() - self.beg < 0.2:
      
      if GPIO.event_detected(12): # fall
        
        timefall = time.time()
        self.log_fall(timefall)
        if (timefall - self.beg) > (self.freq * 1.5):
          timefall = time.time()
        elif (timefall - self.beg) > (self.freq * 0.75): # 0
          self.rcv_bit(0, timefall)
          self.beg = time.time()
          self.log_next()
      if GPIO.event_detected(11): # rise
        timerise = time.time()
        self.log_rise(timerise)
        if (timerise - self.beg) > (self.freq * 0.75): # 1
          self.rcv_bit(1, timerise)
          self.beg = time.time()
          self.log_next()
         
  def read_integer(self, i, nb_bits):
    val = []
    if (i + nb_bits >= self.size):
      return -1
    for j in xrange(i, i + nb_bits):
      if self.is_preempted(j):
        return -1
      val.append(self.msg_data[j])
    return int(''.join(str(x) for x in val), 2)

  def read_sequence_number(self, i):
    self.sequence_number = self.read_integer(i, 4)
    if self.sequence_number == -1:
      return i
    return i+4

  def read_data_size(self, i):
    self.data_size = self.read_integer(i, 6)
    if self.data_size == -1:
      return i
    return i+6
  
  def new_trame(self, i):
    cpt = 0
    while cpt != 8:

      if i <= 0 or i >= self.size:
        cpt = 0
      elif self.msg_t[i] - self.msg_t[i-1] > self.freq * 2: # constant N
        cpt = 0
        
      if i >= self.size:
        return -1
      elif self.msg_data[i] == 1:
        cpt = cpt + 1
      else :
        cpt = 0
      i = i + 1
    return i

  def is_new_msg(self, i):
    cpt = 0
    while cpt != 8:
      if i == self.size:
        return False
      if self.msg_data[i] == 1:
        cpt = cpt + 1
      else :
        return False
      i = i + 1
    return True

  def is_preempted(self, i):
    if i == 0:
      return False
    elif i == self.size:
      return False
    elif self.msg_t[i] - self.msg_t[i-1] > self.freq * 2:
      return True
    else:
      return False

  def build_message(self):
    for i in xrange(1, self.packet_number+1):
      try:
        packet = self.packets[i]['data']
        self.msg += packet
      except KeyError:
        for j in xrange(self.max_data_size):
          self.msg += [0,0,1,1,1,1,1,1] # char '?'
        pass

  def read_packet(self, i):
    save_i = i
    packet = []
    error = False
    for j in xrange(self.size_pl * self.data_size): 
      if self.is_preempted(i):
        error = True
      elif i < self.size:
        packet.append(self.msg_data[i])
        i = i + 1

    if not error:
      for j in xrange(0, len(packet), 8):
        if packet[j] == 1:
          error = True
        
    if not error:
      self.max_data_size = max(self.max_data_size, self.data_size)
      self.packets[self.packet_number] = {'data': packet, 'error': error}
    if error:
      self.packet_number = self.old_packet_number
      self.old_sequence_number = self.older_sequence_number
      return save_i
    return i
  
  def new_packet_number(self):
    self.old_packet_number = self.packet_number
    add = 0
    if self.old_sequence_number < self.sequence_number:
      add = self.sequence_number - self.old_sequence_number
    elif self.old_sequence_number > self.sequence_number: # -> rotation
      add = self.sequence_number - (self.old_sequence_number - (self.max_seq_num+1))
    self.older_sequence_number = self.old_sequence_number
    self.old_sequence_number = self.sequence_number
    self.packet_number += add
     
  def unpack(self):
    self.size = len(self.msg_data)
    self.packets = {}
    self.packet_number = 0
    self.sequence_number = 0
    self.data_size = 0
    self.old_sequence_number = 0
    self.max_data_size = 0
    i = 0
    end = False
    while not end:
      j = self.new_trame(i)
      
      if j != -1: # TRAME
        i = j
        save_i = i

        # Get sequence number
        i = self.read_sequence_number(i)
        if self.sequence_number == -1:
          i = save_i
          continue
        # Get data size
        i = self.read_data_size(i)
        if self.data_size == -1:
          i = save_i
          continue

        # Get packet number
        self.new_packet_number()
        # Read data
        i = self.read_packet(i)
      
      else:
        end = True
    self.build_message()
# =======================
# Lancement du programme
# =======================

if len(sys.argv) < 1:
  sys.exit('Usage: sudo %s' % sys.argv[0])

rcpt = Receptor()
rcpt.sync()
beg_dl = time.time()
rcpt.download()
end_dl = time.time()
print "Frequency : " + str(rcpt.freq) + " s"
print "Laser speed : " + str(len(rcpt.msg_data)/(end_dl - beg_dl)) + " bps"
rcpt.save_log()

rcpt.unpack()
print "Download speed : " + str(len(rcpt.msg)/(end_dl - beg_dl)) + " bps"
if len(rcpt.msg) == 0:
  print 'DL FAILED, please retry'

bin_msg = binaries_to_bytes(rcpt.msg)
save_binary(bin_msg)

GPIO.cleanup()
