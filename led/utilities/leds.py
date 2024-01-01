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

for i in range(0,6):
    ledON(i)
    time.sleep(0.5)

ledAllOFF()
