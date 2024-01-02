import RPi.GPIO as GPIO
from threading import Thread, Event
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

gpio = [25,12,16,20,21]

exit_event = Event()

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
        if exit_event.is_set():
            print("blink break")
            break

def go():
    print("1:",exit_event)
    exit_event.clear()
    print("2:",exit_event)
    print("start")
    t1 = Thread(target = blink, daemon=True)
    t1.start()
    time.sleep(5)
    print("begin stop")
    exit_event.set()
    print("3:",exit_event)
    time.sleep(2)

    print("end")
    ledAllOFF()
    
while True:
    go()
    time.sleep(5)
    
print("OK")



#for i in range(0,6):
#    ledON(i)
#    time.sleep(0.5)

ledAllOFF()
