import serial
import time

a = 0
ser = serial.Serial('/dev/ttyUSB0',9600)

while True:
        ##kirim data
        a = a + 1
        ser.write(str(a))
        print(str(a))
        time.sleep(0.01)

        ##terima data
        ##read_serial=ser.readline()
        ##print read_serial
