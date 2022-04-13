import RPi.GPIO as io
pin = 18

io.setmode(io.BCM)
io.setwarnings(False)
io.setup(pin, io.OUT) ##deklarasi pin OUT/IN
##io.output(pin, io.HIGH) ##digital output HIGH/LOW
p = io.PWM(pin,100)    ##deklarasi PWM   (pin, frequency)

p.start(100)         ##mulai dutycycle 0-100 %
##p.ChangeDutyCycle(100)   ##merubah dutycycle
##p.stop()              ##menghentikan PWM
##io.cleanup()        ##reset kondisi pin ke default
