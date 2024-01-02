#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymbta3 import Stops, Predictions, Routes, Vehicles
from datetime import datetime
import time, sys

#************************************
''' Params '''
#************************************
class Conf:

    refresh_time = 10
    show_location = False

    key = "91944a70800a4bcabe1b9c2023d12fc8"
    rt = Routes(key=key)
    st = Stops(key=key)
    pr = Predictions(key=key)
    vh = Vehicles(key=key)

    if show_location:
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="Angelo")

#************************************
''' Main '''
#************************************
def main():
    if len(sys.argv) < 2:
        print(' Usage:\n  python3 mbta_signs.py <line> <station-code>')
        usage()
        return
    
    dP = Conf()
    line = sys.argv[1]
    station = sys.argv[2]
    
    ############################
    # get coord/name station
    ############################
    s = dP.st.get(route=line, id=station)['data'][0]['attributes']
    la = s['latitude']
    lo = s['longitude']
    name = s['name']
    print("\n")

    while True:
        pred = dP.pr.get(longitude=lo, latitude=la, radius=0.001)['data']
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
                v = dP.vh.get(id=p['relationships']['vehicle']['data']['id'])['data'][0]['attributes']
                vtype.append(train_type(line,v))
                vstatus.append(v['current_status'])
                vstation.append(get_stat(line, v['latitude'], v['longitude']))
                if dP.show_location:
                    location.append(dP.geolocator.reverse(str(v['latitude'])+','+str(v['longitude'])))
                dummy += 1
           
        print("-------------------------------------------------------------------------")
        print("\033[1m"+name+"\033[0m\t\t",current_time)
        print("-------------------------------------------------------------------------")
        for j in range(0,len(direction)):
            if direction[j] == 0:
                arr_sign(pred_arr_times[j], get_dir(line, direction[j]), vstatus[j], vstation[j], vtype[j])
        print("-------------------------------------------------------------------------")
        for j in range(0,len(direction)):
            if direction[j] == 1:
                arr_sign(pred_arr_times[j], get_dir(line, direction[j]), vstatus[j], vstation[j], vtype[j])
        print("-------------------------------------------------------------------------")
        print("\n")
        if dP.show_location:
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
    
        time.sleep(dP.refresh_time)

########################
# Definitions
########################
def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)
    
def get_dir(line, a):
    return Conf().rt.get(id=line)['data'][0]['attributes']['direction_destinations'][a]

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

def get_stat(line, la, lo):
    s = Conf().st.get(route=line, longitude=lo, latitude=la, radius=0.005)['data']
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

            

