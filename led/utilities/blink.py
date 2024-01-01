import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

gpio = [25,12,16,20,21]

for i in range(len(gpio)):
   GPIO.setup(gpio[i],GPIO.OUT)
    
def ledON(num):
    for j in range(num):
        GPIO.output(gpio[j],GPIO.HIGH)
        
def ledAllOFF():
    for i in range(len(gpio)):
        GPIO.output(gpio[i],GPIO.LOW)

def blink(a):
    t = 0
    while t < a:
        GPIO.output(gpio[4],GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(gpio[4],GPIO.LOW)
        time.sleep(0.5)
        t += 1
        if t > a:
            break

a = 5
blink(a)
a = False
print("OK")



#for i in range(0,6):
#    ledON(i)
#    time.sleep(0.5)

ledAllOFF()
