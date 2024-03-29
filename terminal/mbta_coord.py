#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************
* MBTA COORD
* v2024.01.15.1
* By: Nicola Ferralis <feranick@hotmail.com>
**********************************************
'''
#print(__doc__)

#from pymbta3 import Stops, Predictions, Routes, Vehicles
from datetime import datetime
import time, sys, requests

#***************************************************
# This is needed for installation through pip
#***************************************************
def mbta_coord():
    main()

#************************************
''' Params '''
#************************************
class Conf:
    def __init__(self):
        self.refresh_time = 10
        self.list_items = 10
        self.show_location = False

        self.key = "91944a70800a4bcabe1b9c2023d12fc8"
        #self.rt = Routes(key=self.key)
        #self.st = Stops(key=self.key)
        #self.pr = Predictions(key=self.key)
        #self.vh = Vehicles(key=self.key)
        
        self.url = "https://api-v3.mbta.com/"
        self.headers = {'Accept': 'application/json', 'x-api-key': self.key}
        #self.auth = HTTPBasicAuth('apikey', self.key)
        
        if self.show_location:
            from geopy.geocoders import Nominatim
            self.geolocator = Nominatim(user_agent="Angelo")

#************************************
''' Main '''
#************************************
def main():
    if len(sys.argv) < 3:
        print(' Usage:\n  python3 mbta_coord.py <long> <lat>')
        usage()
        return
    dP = Conf()
    lo = sys.argv[1]
    la = sys.argv[2]
    name = []
    
    st_url = dP.url+"stops/?filter[longitude]="+lo+"&filter[latitude]="+la+"&filter[radius]=0.001"
    st = requests.get(st_url,headers=dP.headers).json()['data']
    
    
    # Change to make multiple predictions for each station.
    #for s in st:
    #    name.append(s['attributes']['name'])
    
    if len(st) > 0:
        print("\n Number of stations in this area:",len(st))
        name = st[0]['attributes']['name']
    else:
        print("\n No station found")
        name = ""
    print(name)
    
    print("\n")

    while True:
        #pred = dP.pr.get(longitude=lo, latitude=la, radius=0.001)['data']
        pr_url = dP.url+"predictions/?filter[longitude]="+lo+"&filter[latitude]="+la+"&filter[radius]=0.001"
        pred = requests.get(pr_url,headers=dP.headers).json()['data']
            
        if len(pred) == 0:
            print(" No data currently available. Try again later.")
            print(" Possible cause: no service available at this time\n")
            break
        dummy = 0
        pred_arr_times = []
        direction = []
        status = []
        vstation = []
        vstatus = []
        vtype = []
        location = []
        lines = []
    
        for p in pred:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            id_line = p['relationships']['route']['data']['id']
            #if id_line in line and dummy < dP.list_items:
            if dummy < dP.list_items:
                try:
                    arr_time = p['attributes']['arrival_time'][11:][:8]
                    dep_time = p['attributes']['departure_time'][11:][:8]
                    arr_time_mins = (get_sec(arr_time) - get_sec(current_time))/60
                    dep_time_mins = (get_sec(dep_time) - get_sec(current_time))/60
                
                    #v = dP.vh.get(id=p['relationships']['vehicle']['data']['id'])['data'][0]['attributes']
                    vh_url = dP.url+"vehicles/?filter[id]="+p['relationships']['vehicle']['data']['id']
                    v = requests.get(vh_url,headers=dP.headers).json()['data'][0]
                    
                    lines.append(id_line)
                    pred_arr_times.append(arr_time_mins)
                    direction.append(p['attributes']['direction_id'])
                    status.append(p['attributes']['status'])
                    vtype.append(train_type(id_line,v['attributes']))
                    vstatus.append(v['attributes']['current_status'])
                    vstation.append(get_stop(v['relationships']['stop']['data']['id']))
                    if dP.show_location:
                        location.append(dP.geolocator.reverse(str(v['attributes']['latitude'])+','+str(v['attributes']['longitude'])))
                except:
                    pass
                dummy += 1
        
        print("-----------------------------------------------------------------------------------------")
        print("\033[1m"+name+"\033[0m\t\t",current_time)
        print("-----------------------------------------------------------------------------------------")
        for j in range(0,len(direction)):
            if direction[j] == 0:
                arr_sign(pred_arr_times[j], get_dir(lines[j], direction[j]), vstatus[j], vstation[j], vtype[j], lines[j])
        print("-----------------------------------------------------------------------------------------")
        for j in range(0,len(direction)):
            if direction[j] == 1:
                arr_sign(pred_arr_times[j], get_dir(lines[j], direction[j]), vstatus[j], vstation[j], vtype[j], lines[j])
        print("-----------------------------------------------------------------------------------------")
        print("\n")
        if dP.show_location:
            print("-----------------------------------------------------------------------------------------")
            for j in range(0,len(direction)):
                if direction[j] == 0:
                    print(location[j])
            print("-----------------------------------------------------------------------------------------")
            for j in range(0,len(direction)):
                if direction[j] == 1:
                    print(location[j])
            print("-----------------------------------------------------------------------------------------")
            print("\n")
    
        time.sleep(dP.refresh_time)

########################
# Definitions
########################
def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)
    
def get_dir(line, a):
    #return Conf().rt.get(id=line)['data'][0]['attributes']['direction_destinations'][a]
    rt_url = Conf().url+"routes/?filter[id]="+line
    return requests.get(rt_url,headers=Conf().headers).json()['data'][0]['attributes']['direction_destinations'][a]

def arr_sign(a, b, st, station, type, line):
    if a > 0 and a < 0.5:
        print(b,"\t ARR\t",type,"\t",line,"\t", st, station)
    if a > 0.5 and a < 1:
        print(b,"\t APPR\t",type,"\t",line,"\t", st, station)
    if a >= 1:
        print(b,"\t",round(a),"min\t",type,"\t",line,"\t", st, station)
    if a>-10 and a<= 0:
        print(b,"\t BOARD\t",type,"\t",line,"\t", st, station)
    if a<=-10:
        print(b,"\t ---\t",type,"\t",line,"\t", st, station)
        
def get_stop(stop):
    #st = Stops(key=Conf().key)
    #s = st.get(route='Red', longitude=lo, latitude=la, radius=0.005)['data']
    #st_url = Conf().url+"stops/?filter[longitude]="+str(lo)+"&filter[latitude]="+str(la)+"&filter[radius]=0.001"
    #st_url = Conf().url+"stops/?filter[route]="+line+"&filter[id]="+stop
    st_url = Conf().url+"stops/?filter[id]="+stop
    s = requests.get(st_url,headers=Conf().headers).json()['data']
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
    
def find_routes_through_station(station):
    lines = []
    #st = Stops(key=Conf().key)
    #rt = Routes(key=Conf().key)
    #routes = rt.get()['data']
    routes = requests.get(Conf().url+"routes/",headers=Conf().headers).json()['data']
    
    print("\n Searching for routes passing through:",station,"\n Please wait...\n")
    for r in routes:
    
        #stops = st.get(route=r['id'])['data']
        stops = requests.get(Conf().url+"stops/?filter[route]="+r['id'],headers=Conf().headers).json()['data']
        
        for s in stops:
            if s['id'] == station:
                lines.append(r['id'])
    
    print(" ".join(lines),"\n")
    return lines
        
#************************************
# Lists the stations and lines
#************************************
def usage():
    print(__doc__)
    print(' List of stations and lines\n')
    print(' Red-Central: place-cntsq Red')
    print(' Red-Kendall: place-knncl Red ')
    print(' Red-ParkSt: place-pktrm Red ')
    print(' Red-CharlesMGH: place-chmnl Red ')
    print(' Green-D-Lechmere : place-lech Green-D ')
    print(' Green-D-Union Sq : place-unsqu Green-D')
    print(' Green-E-Medford : place-medftf Green-D ')
    print(' Orange-Ruggles : place-rugg Orange ')
    print(' Orange-Sullivan : place-sull Orange ')
    print(' CR-Providence-Ruggles : place-rugg CR-Providence')
    print(' CR-Providence-South Station : place-sstat CR-Providence ')
    print(' Silver Line 1 - Airport : 17095 74`')
    print(' Bus-1 Stop 72 : 72 1\n')
    
#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())

            

