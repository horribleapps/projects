import serial
import time

def move_obj(distance,speed,axis):
    ser=serial.Serial("/dev/ttyUSB0",115200,timeout=1)
    #ser.write(b'$\n')
    #time.sleep(5)
    ser.write(b'G91\n')
    time.sleep(5)
    gcodestr=f'G1 {axis}{distance} F{speed}\n'
    ser.write(gcodestr.encode('ASCII'))
    time.sleep(5)
    time.sleep(int(abs(distance)/speed*60)+5)
    ser.close()

def main():
    move_obj(-30,100,'Y')

if __name__ == "__main__":
    main()
