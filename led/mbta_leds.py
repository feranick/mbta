#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymbta3 import Stops, Predictions
from threading import Thread, Event
from datetime import datetime
import time, sys
import RPi.GPIO as GPIO


#************************************
''' Params '''
#************************************
class Conf:
    key = "91944a70800a4bcabe1b9c2023d12fc8"

    refresh_time = 1
    gpio = [25,12,16,20,21]

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for i in range(len(gpio)):
        GPIO.setup(gpio[i],GPIO.OUT)
        
    stop_blinkLed = Event()
    stop_blinkAllLed = Event()

    st = Stops(key=key)
    pr = Predictions(key=key)

#************************************
# Main
#************************************
def main():
    if len(sys.argv) < 4:
        print(' Usage:\n python3 mbta_signs.py <line> <station-code> <direction>')
        usage()
        return
        
    dP = Conf()
    line = sys.argv[1]
    station = sys.argv[2]
    direct = int(sys.argv[3])
            
    ############################
    # get coord/name station
    ############################
    s = dP.st.get(route=line, id=station)['data'][0]['attributes']
    la = s['latitude']
    lo = s['longitude']
    name = s['name']
    print("\n")

    ############################
    # Loop
    ############################
    t1 = Thread(target = blinkLed)
    t2 = Thread(target = blinkAllLed)
    
    while True:
        pred = dP.pr.get(longitude=lo, latitude=la, radius=0.001)['data']
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
                arr_sign(pred_arr_times[ind], t1, t2)
                break
            ind += 1

        time.sleep(dP.refresh_time)
            

########################
# Definitions
########################
def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)
        
def ledAllOFF():
    for i in range(len(Conf().gpio)):
        GPIO.output(Conf().gpio[i],GPIO.LOW)
        
def ledAllON():
    for i in range(len(Conf().gpio)):
        GPIO.output(Conf().gpio[i],GPIO.HIGH)
        
def ledON(num):
    for j in range(round(num)):
        GPIO.output(Conf().gpio[j],GPIO.HIGH)
        
def blinkLed():
    while True:
        GPIO.output(Conf().gpio[0],GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(Conf().gpio[0],GPIO.LOW)
        time.sleep(0.5)
        print("stop_blinkLed:",stop_blinkLed)
        if Conf().stop_blinkLed.is_set():
            print("stopped")
            break

def blinkAllLed():
    print("backend",Conf().stop_blinkAllLed)
    while True:
        ledAllON()
        time.sleep(0.5)
        ledAllOFF()
        time.sleep(0.5)
        print("stop_blinkAllLed:",Conf().stop_blinkAllLed)
        if Conf().stop_blinkAllLed.is_set():
            print("stopped all")
            break

def arr_sign(a, t1, t2):
    print("a:",a)
    ledAllOFF()
    if a>5:
        a = 5
    if a>0:
        print("a>0")
        if a>1:
            print("a>1")
            if t1.is_alive():
                Conf().stop_blinkLed.set()
                t1.join()
            if t2.is_alive():
                Conf().stop_blinkAllLed.set()
                t2.join()
            ledON(int(a))
        else:
            print("a<1")
            if t1.is_alive() == False:
                Conf().stop_blinkLed.clear()
                t1.start()
            if t2.is_alive():
                Conf().stop_blinkAllLed.set()
                t2.join()
    if a<=0:
        print("a<=0")
        if t1.is_alive():
            Conf().stop_blinkLed.set()
            t1.join()
        if t2.is_alive() == False:
            Conf().stop_blinkAllLed.clear()
            t2.start()

#************************************
# Lists the stations and lines
#************************************
def usage():
    print('\n List of stations and lines\n')
    print(' Red-Central: Red place-cntsq')
    print(' Red-Kendall: Red place-knncl')
    print(' Red-CharlesMGH: Red place-chmnl')
    print(' Green-D-Lechmere : Green-D place-lech')
    print(' Green-D-Union Sq : Green-D place-unsqu')
    print(' Green-E-Medford : Green-D place-medftf')
    print(' Orange-Ruggles : Orange place-rugg')
    print(' Orange-Sullivan : Orange place-sull')
    print(' CR-Providence-Ruggles : CR-Providence place-rugg')
    print(' CR-Providence-South Station : CR-Providence place-sstat')
    print(' Silver Line 1 - Airport : 741 17095')
    print(' Bus-1 Stop 72 : 1 72\n')
    
#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
