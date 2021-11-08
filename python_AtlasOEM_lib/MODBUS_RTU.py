import serial
import time

receiver = serial.Serial(     
     port='/dev/ttyS0',        
     baudrate = 115200,
     parity=serial.PARITY_NONE,
     stopbits=serial.STOPBITS_ONE,
     bytesize=serial.EIGHTBITS,
     timeout=1
     )

while 1:
      x = receiver.readline()
      print (x)