#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************
* MBTA VEHICLES
* v2024.01.03.1
* By: Nicola Ferralis <feranick@hotmail.com>
**********************************************
'''
#print(__doc__)

from pymbta3 import Stops, Vehicles
from geopy.geocoders import Nominatim
import sys

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
        self.key = "91944a70800a4bcabe1b9c2023d12fc8"

#************************************
''' Main '''
#************************************
def main():
    vh = Vehicles(key=Conf().key)
    vehicles = vh.get()['data']
    for v in vehicles:
        #print(v['relationships']['route']['data']['id'])
        if v['relationships']['route']['data']['id'] == 'Red':
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
    st = Stops(key=Conf().key)
    s = st.get(route='Red', longitude=lo, latitude=la, radius=0.005)['data']
    if len(s) == 0:
        return ''
    else:
        return s[0]['attributes']['name']

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
