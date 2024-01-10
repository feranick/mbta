#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************
* MBTA LEDS SIMPLE
* v2024.01.10.1
* By: Nicola Ferralis <feranick@hotmail.com>
**********************************************
'''
#print(__doc__)

#from pymbta3 import Stops, Predictions
from threading import Thread, Event
from datetime import datetime
import time, sys, requests
import RPi.GPIO as GPIO

#***************************************************
# This is needed for installation through pip
#***************************************************
def mbta_leds_simple():
    main()

#************************************
''' Params '''
#************************************
class Conf:
    def __init__(self):
        self.key = "91944a70800a4bcabe1b9c2023d12fc8"
        self.url = "https://api-v3.mbta.com/"
        self.headers = {'Accept': 'application/json', 'x-api-key': self.key}

        self.refresh_time = 5
        self.list_items = 4
        self.gpio = [25,12,16,20,21]

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for i in range(len(self.gpio)):
            GPIO.setup(self.gpio[i],GPIO.OUT)
        
        self.stop_blinkLed = Event()
        self.stop_blinkAllLed = Event()

        #self.st = Stops(key=self.key)
        #self.pr = Predictions(key=self.key)

#************************************
# Main
#************************************
def main():
    if len(sys.argv) < 4:
        print(' Usage:\n python3 mbta_leds.py <station-code> <line> <direction>')
        usage()
        return
        
    dP = Conf()
    station = sys.argv[1]
    line = sys.argv[2]
    direct = int(sys.argv[3])
                
    ############################
    # get coord/name station
    ############################
    
    try:
        #s = dP.st.get(route=line, id=station)['data'][0]['attributes']
        st_url = dP.url+"stops/?filter[route]="+line[0]+"&filter[id]="+station
        s = requests.get(st_url).json()['data'][0]['attributes']
    except:
        print("\n These lines do not stop at this station\n")
        return
    
    la = s['latitude']
    lo = s['longitude']
    name = s['name']
    print("\n")

    ############################
    # Loop
    ############################
    t1 = Thread(target = blinkLed, args=(dP,), daemon=True)
    t2 = Thread(target = blinkAllLed, args=(dP,), daemon=True)

    while True:
        #pred = dP.pr.get(longitude=lo, latitude=la, radius=0.001)['data']
        pr_url = dP.url+"predictions/?filter[longitude]="+lo+"&filter[latitude]="+la+"&filter[radius]=0.001"
        pred = requests.get(pr_url,headers=dP.headers).json()['data']
        
        dummy = 0
        pred_arr_times = []
        direction = []

        for p in pred:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            if p['relationships']['route']['data']['id'] == line and dummy < dP.list_items:
                try:
                    arr_time = p['attributes']['arrival_time'][11:][:8]
                    dep_time = p['attributes']['departure_time'][11:][:8]
                    arr_time_mins = (get_sec(arr_time) - get_sec(current_time))/60
                    dep_time_mins = (get_sec(dep_time) - get_sec(current_time))/60
                    pred_arr_times.append(arr_time_mins)
                    direction.append(p['attributes']['direction_id'])
                except:
                    pass
                dummy += 1
        ind = 0
        for dir in direction:
            if dir == direct:
                t1, t2 = arr_sign(pred_arr_times[ind], dP, t1, t2)
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
        
def blinkLed(dP):
    ledAllOFF()
    while True:
        GPIO.output(Conf().gpio[0],GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(Conf().gpio[0],GPIO.LOW)
        time.sleep(0.5)
        if dP.stop_blinkLed.is_set():
            break

def blinkAllLed(dP):
    while True:
        ledAllON()
        time.sleep(0.5)
        ledAllOFF()
        time.sleep(0.5)
        if dP.stop_blinkAllLed.is_set():
            break

def arr_sign(a, dP, t1, t2):
    dP.stop_blinkLed.clear()
    dP.stop_blinkAllLed.clear()
    if a>5:
        a = 5
    if a>0:
        if a>1:
            if t1.is_alive():
                dP.stop_blinkLed.set()
                t1.join()
            if t2.is_alive():
                dP.stop_blinkAllLed.set()
                t2.join()
            ledAllOFF()
            ledON(int(a))
        else:
            if t1.is_alive() == False:
                dP.stop_blinkLed.clear()
                t1 = Thread(target = blinkLed, args=(dP,), daemon=True)
                t1.start()
            if t2.is_alive():
                dP.stop_blinkAllLed.set()
                t2.join()
    if a<=0:
        if t1.is_alive():
            dP.stop_blinkLed.set()
            t1.join()
        if t2.is_alive() == False:
            dP.stop_blinkAllLed.clear()
            t2 = Thread(target = blinkAllLed, args=(dP,), daemon=True)
            t2.start()
    return t1, t2
            
#************************************
# Lists the stations and lines
#************************************
def usage():
    print(__doc__)
    print(' List of stations and lines\n')
    print(' Red-Central: place-cntsq Red 1')
    print(' Red-Kendall: place-knncl Red 1')
    print(' Red-ParkSt: place-pktrm Red 0')
    print(' Red-CharlesMGH: place-chmnl Red 1')
    print(' Green-D-Lechmere : place-lech Green-D 1')
    print(' Green-D-Union Sq : place-unsqu Green-D 0')
    print(' Green-E-Medford : place-medftf Green-D 1')
    print(' Orange-Ruggles : place-rugg Orange 1')
    print(' Orange-Sullivan : place-sull Orange 0')
    print(' CR-Providence-Ruggles : place-rugg CR-Providence 0')
    print(' CR-Providence-South Station : place-sstat CR-Providence 1')
    print(' Silver Line 1 - Airport : 17095 74 1')
    print(' Bus-1 Stop 72 : 72 1 0\n')

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
