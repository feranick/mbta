#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymbta3 import Stops, Predictions, Routes, Vehicles
from threading import Thread, Event
from datetime import datetime
import time
import RPi.GPIO as GPIO
import time

key = "91944a70800a4bcabe1b9c2023d12fc8"

#station = 'place-cntsq'
station = 'place-knncl'
#station = 'place-chmnl'
line = 'Red'
direct = 1

refresh_time = 1
show_location = False
gpio = [25,12,16,20,21]

stop_blinkLed = Event()
stop_blinkAllLed = Event()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for i in range(len(gpio)):
   GPIO.setup(gpio[i],GPIO.OUT)

rt = Routes(key=key)
st = Stops(key=key)
pr = Predictions(key=key)
vh = Vehicles(key=key)

########################
# Definitions
########################
def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)
        
def ledAllOFF():
    for i in range(len(gpio)):
        GPIO.output(gpio[i],GPIO.LOW)
        
def ledAllON():
    for i in range(len(gpio)):
        GPIO.output(gpio[i],GPIO.HIGH)
        
def ledON(num):
    for j in range(round(num)):
        GPIO.output(gpio[j],GPIO.HIGH)
        
def blinkLed():
    while True:
        GPIO.output(gpio[0],GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(gpio[0],GPIO.LOW)
        time.sleep(0.5)
        print("stop_blinkLed:",stop_blinkLed)
        if stop_blinkLed.is_set():
            print("stopped")
            break

def blinkAllLed():
    print("backend",stop_blinkAllLed)
    while True:
        ledAllON()
        time.sleep(0.5)
        ledAllOFF()
        time.sleep(0.5)
        print("stop_blinkAllLed:",stop_blinkAllLed)
        if stop_blinkAllLed.is_set():
            print("stopped all")
            break

def arr_sign(a):
    t1 = Thread(target = blinkLed, args=(stop_blinkLed,))
    t2 = Thread(target = blinkAllLed, args=(stop_blinkAllLed,))
    print("a:",a)
    ledAllOFF()
    if a>5:
        a = 5
    if a>0:
        print("a>0")
        if a>1:
            print("a>1")
            if t1.is_alive():
                print("a>1, stop blinkLed")
                stop_blinkLed.is_set()
                t1.join()
            if t2.is_alive():
                print("a>1, stop blinkAllLed")
                stop_blinkAllLed.is_set()
                t2.join()
            ledON(int(a))
        else:
            print("a<1")
            if t1.is_alive() == False:
                print("a<1, start blinkLed")
                stop_blinkLed.clear()
                t1.start()
            if t2.is_alive():
                print("a<1, stop blinkAllLed")
                stop_blinkAllLed.is_set()
                t2.join()
    if a<=0:
        print("a<=0")
        if t1.is_alive():
            print("a<0, stop blinkLed")
            stop_blinkLed.is_set()
            t1.join()
        if t2.is_alive() == False:
            print("a<0, start blinkAllLed")
            stop_blinkAllLed.clear()
            t2.start()

############################
# get coord/name station
############################
s = st.get(route=line, id=station)['data'][0]['attributes']
la = s['latitude']
lo = s['longitude']
name = s['name']
print("\n")

############################
# Loop
############################

while True:
    pred = pr.get(longitude=lo, latitude=la, radius=0.001)['data']
    dummy = 0
    pred_arr_times = []
    direction = []
    
    for p in pred:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if p['relationships']['route']['data']['id'] == line and dummy < 8:
            try:
                arr_time = p['attributes']['arrival_time'][11:][:8]
                dep_time = p['attributes']['departure_time'][11:][:8]
            except:
                arr_time = "00:00:00"
                dep_time = "00:00:00"
            arr_time_mins = (get_sec(arr_time) - get_sec(current_time))/60
            dep_time_mins = (get_sec(dep_time) - get_sec(current_time))/60
            pred_arr_times.append(arr_time_mins)
            direction.append(p['attributes']['direction_id'])
            dummy += 1
    ind = 0

    for dir in direction:
        if dir == direct:
            arr_sign(pred_arr_times[ind])
            break
        ind += 1

    time.sleep(refresh_time)
            

