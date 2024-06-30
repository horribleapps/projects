import serial
import time
ser=serial.Serial("/dev/ttyUSB0",115200,timeout=1)
#ser.write(b'$\n')
#time.sleep(5)
ser.write(b'G91\n')
time.sleep(5)
ser.write(b'G1 Y50 F100\n')
time.sleep(5)
ser.close()
