#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************
* MBTA VEHICLES
* v2024.01.04.1
* By: Nicola Ferralis <feranick@hotmail.com>
**********************************************
'''
#print(__doc__)

#from pymbta3 import Stops, Vehicles
from geopy.geocoders import Nominatim
import sys, requests

#***************************************************
# This is needed for installation through pip
#***************************************************
def mbta_vehicles():
    main()
    
#************************************
''' Params '''
#************************************
class Conf:
    def __init__(self):
        self.url = "https://api-v3.mbta.com/"
        self.key = "91944a70800a4bcabe1b9c2023d12fc8"
        self.headers = {'Accept': 'application/json', 'x-api-key': self.key}

#************************************
''' Main '''
#************************************
def main():
    #vh = Vehicles(key=Conf().key)
    #vehicles = vh.get()['data']
    vehicles = requests.get(Conf().url+"vehicles/",headers=Conf().headers).json()['data']
    
    for v in vehicles:
        #print(v['relationships']['route']['data']['id'])
        if v['relationships']['route']['data']['id'] == 'Red':
            print(v)
            la = v['attributes']['latitude']
            lo = v['attributes']['longitude']
            print(v['id'])
            print(v['attributes']['current_status'], get_stat(la, lo))
            print("Stop sequence:",v['attributes']['current_stop_sequence'])
            print("Bearing: ",v['attributes']['bearing'])
            print("Latitude:",la,", Longitude:",lo)
            print("Speed:",v['attributes']['speed'])
        
            coord = str(v['attributes']['latitude'])+','+str(v['attributes']['longitude'])
            geolocator = Nominatim(user_agent="Angelo")
            print(coord)
            #location = geolocator.reverse("42.39618,-71.02866")
            location = geolocator.reverse(coord)
            print(location)
            print("\n")
        
def get_stat(la, lo):
    #st = Stops(key=Conf().key)
    #s = st.get(route='Red', longitude=lo, latitude=la, radius=0.005)['data']
    st_url = Conf().url+"stops/?filter[route]="+"Red"+"&filter[longitude]="+str(lo)+"&filter[latitude]="+str(la)+"&filter[radius]=0.001"
    s = requests.get(st_url,headers=Conf().headers).json()['data']
    if len(s) == 0:
        return ''
    else:
        return s[0]['attributes']['name']

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
