#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************
* MBTA STOP ID
* v2024.01.04.3
* By: Nicola Ferralis <feranick@hotmail.com>
**********************************************
'''
#print(__doc__)

import sys, requests

#***************************************************
# This is needed for installation through pip
#***************************************************
def mbta_stop_id():
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
        print('\n Usage:\n  python3 mbta_stop_id.py <vehicle_id>')
        print('  python3 gfts_vehicles.py list \n   To list MBTA fleet\n')
        return
        
    if sys.argv[1] == "list":
        vehicles = requests.get(Conf().url+"vehicles/",headers=Conf().headers).json()['data']
        for v in vehicles:
            print(v['attributes']['label'], v['id'])
        return
    
    s = requests.get(Conf().url+"stops/?filter[id]="+sys.argv[1], headers=Conf().headers).json()['data'][0]

    print("\n Stop ID:", sys.argv[1])
    print(" Stop name:",s['attributes']['name'])
    print(" Address:",s['attributes']['address'])
    print(" Municipality:",s['attributes']['municipality'])
    print(" Latitude:",s['attributes']['latitude'])
    print(" Longitude:",s['attributes']['longitude'])
    print(" Routes through station:"," ".join(find_routes_through_station(sys.argv[1])))
    print("\n")
        
    stops = requests.get(Conf().url+"stops/",headers=Conf().headers).json()['data']
        
def find_routes_through_station(station):
    lines = []
    routes = requests.get(Conf().url+"routes/",headers=Conf().headers).json()['data']
    print("\n Searching for routes passing through:",station,"\n Please wait...\n")
    for r in routes:
        stops = requests.get(Conf().url+"stops/?filter[route]="+r['id'],headers=Conf().headers).json()['data']
        for s in stops:
            if s['id'] == station:
                lines.append(r['id'])
    #print(" ".join(lines),"\n")
    return lines

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
