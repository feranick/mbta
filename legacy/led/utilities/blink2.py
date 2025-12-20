import RPi.GPIO as GPIO
from threading import Thread
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

gpio = [25,12,16,20,21]

global stop_blinkLed

for i in range(len(gpio)):
   GPIO.setup(gpio[i],GPIO.OUT)
    
def ledON(num):
    for j in range(num):
        GPIO.output(gpio[j],GPIO.HIGH)
        
def ledAllOFF():
    for i in range(len(gpio)):
        GPIO.output(gpio[i],GPIO.LOW)

def blink():
    while True:
        GPIO.output(gpio[4],GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(gpio[4],GPIO.LOW)
        time.sleep(0.5)
        if stop_blinkLed:
            break

stop_blinkLed = False
print("yes")
t1 = Thread(target = blink)
t1.start()
time.sleep(5)
stop_blinkLed = True
t1.join()
    

print("OK")



#for i in range(0,6):
#    ledON(i)
#    time.sleep(0.5)

ledAllOFF()
