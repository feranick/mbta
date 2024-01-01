#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymbta3 import Stops, Predictions, Routes, Vehicles
from datetime import datetime
import time

key = "91944a70800a4bcabe1b9c2023d12fc8"

#station = 'place-sstat'
station = 'place-rugg'
line = 'CR-Providence'

refresh_time = 10
show_location = False

rt = Routes(key=key)
st = Stops(key=key)
pr = Predictions(key=key)
vh = Vehicles(key=key)

if show_location:
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="Angelo")

########################
# Definitions
########################
def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)
    
def get_dir(a):
    return rt.get(id=line)['data'][0]['attributes']['direction_destinations'][a]

def arr_sign(a, b, st, station, type):
    if a > 0 and a < 0.5:
        print(b,"\t ARR\t",type,"\t", st, station)
    if a > 0.5 and a < 1:
        print(b,"\t APPR\t",type,"\t", st, station)
    if a >= 1:
        print(b,"\t",round(a),"min\t",type,"\t", st, station)
    if a>-2 and a<= 0:
        print(b,"\t BOARD\t",type,"\t", st, station)
    if a<=-2:
        print(b,"\t ERR\t",type,"\t", st, station)

def get_stat(la, lo):
    s = st.get(route=line, longitude=lo, latitude=la, radius=0.005)['data']
    if len(s) == 0:
        return ''
    else:
        return s[0]['attributes']['name']
        
def train_type(line, veh):
    try:
        code = int(veh['carriages'][0]['label'])
    except:
        code = int(veh['label'])
    if line == "Red":
        if code < 1800:
            return "O1"
        if code >= 1800 and code < 1900:
            return "O2"
        if code >= 1900:
            return "N"
    if line == "Orange":
        if code < 1400:
            return "O"
        if code >= 1400:
            return "N"
    if line[:5] == "Green":
        if code < 3900:
            return "O"
        if code >= 3900:
            return "N"
    if line[:2] == "CR":
        return "CR"
    else:
        return str(code)
        
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
    status = []
    vstation = []
    vstatus = []
    vtype = []
    location = []
    
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
            #direction.append(get_dir(p['attributes']['direction_id']))
            direction.append(p['attributes']['direction_id'])
            status.append(p['attributes']['status'])
            v = vh.get(id=p['relationships']['vehicle']['data']['id'])['data'][0]['attributes']
            vtype.append(train_type(line,v))
            vstatus.append(v['current_status'])
            vstation.append(get_stat(v['latitude'], v['longitude']))
            if show_location:
                location.append(geolocator.reverse(str(v['latitude'])+','+str(v['longitude'])))
            dummy += 1
           
    print("-------------------------------------------------------------------------")
    print("\033[1m"+name+"\033[0m\t\t",current_time)
    print("-------------------------------------------------------------------------")
    for j in range(0,len(direction)):
        if direction[j] == 0:
            arr_sign(pred_arr_times[j], get_dir(direction[j]), vstatus[j], vstation[j], vtype[j])
    print("-------------------------------------------------------------------------")
    for j in range(0,len(direction)):
        if direction[j] == 1:
            arr_sign(pred_arr_times[j], get_dir(direction[j]), vstatus[j], vstation[j], vtype[j])
    print("-------------------------------------------------------------------------")
    print("\n")
    if show_location:
        print("-------------------------------------------------------------------------")
        for j in range(0,len(direction)):
            if direction[j] == 0:
                print(location[j])
        print("-------------------------------------------------------------------------")
        for j in range(0,len(direction)):
            if direction[j] == 1:
                print(location[j])
        print("-------------------------------------------------------------------------")
        print("\n")
    
    time.sleep(refresh_time)
            

