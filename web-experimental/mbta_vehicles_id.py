#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************
* MBTA VEHICLES ID
* v2024.01.10.1
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
def mbta_vehicles_id():
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
    if len(sys.argv) < 2:
        print(__doc__)
        print(' Usage:\n  python3 mbta_vehicles_id.py <vehicle_id>')
        print('  python3 gfts_vehicles.py list \n   To list MBTA fleet\n')
        return
        
    if sys.argv[1] == "list":
        vehicles = requests.get(Conf().url+"vehicles/",headers=Conf().headers).json()['data']
        for v in vehicles:
            print(v['attributes']['label'], v['id'])
        return
    
    #vh = Vehicles(key=Conf().key)
    #vehicles = vh.get()['data']
    vh = requests.get(Conf().url+"vehicles/?filter[label]="+sys.argv[1], headers=Conf().headers).json()['data']
    
    if len(vh) == 0:
        print("\n No Vehicle with this ID currently in operation\n")
    
    for v in vh:
        print("\n Vehicle label:", sys.argv[1])
        print(" Vehicle ID:", v['id'])
        print(" Route:",v['relationships']['route']['data']['id'])
        print(" Occupancy:",v['attributes']['occupancy_status'])
        print(" Longitude:",v['attributes']['longitude'])
        print(" Latitude: ",v['attributes']['latitude'])
        print(" Bearing: ",v['attributes']['bearing'])
        print(" Speed:",v['attributes']['speed'])
        print(" Stop sequence:",v['attributes']['current_stop_sequence'])
        print(" Status: ",v['attributes']['current_status'],get_stop(v['relationships']['stop']['data']['id']),"(Stop ID:",v['relationships']['stop']['data']['id']+")")
        print(" Time:",v['attributes']['updated_at'])
        
        coord = str(v['attributes']['latitude'])+','+str(v['attributes']['longitude'])
        geolocator = Nominatim(user_agent="Angelo")
        location = geolocator.reverse(coord)
        print("\n",location)
        print("\n")
        
def get_stop(stop):
    #st = Stops(key=Conf().key)
    #s = st.get(route='Red', longitude=lo, latitude=la, radius=0.005)['data']
    #st_url = Conf().url+"stops/?filter[longitude]="+str(lo)+"&filter[latitude]="+str(la)+"&filter[radius]=0.001"
    st_url = Conf().url+"stops/?filter[id]="+stop
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
