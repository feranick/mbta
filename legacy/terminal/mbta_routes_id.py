#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************
* MBTA ROUTES ID
* v2024.01.04.1
* By: Nicola Ferralis <feranick@hotmail.com>
**********************************************
'''
#print(__doc__)

#from pymbta3 import Routes
import sys, requests

#***************************************************
# This is needed for installation through pip
#***************************************************
def mbta_routes_id():
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
    dP = Conf()
    print("\n Type:")
    print("  0	Light Rail	Green Line")
    print("  1	Heavy Rail	Red Line")
    print("  2	Commuter Rail")
    print("  3	Bus")
    print("  4	Ferry")
    print("\n Use mbta_stops.py for codes of stops for a given route")
    print("\n Input router type:")

    type = input()

    # Find all Route data for the Red Line
    #rt = Routes(key=dP.key)
    #routes = rt.get(type=type)['data']
    #routes = rt.get(id='Red')['data']
    #for r in routes:
    #    print(r)
    routes = requests.get(dP.url+"routes/",headers=dP.headers).json()['data']
    
    print("\n ID, short_name")
    for r in routes:
        print(" ",r['id'], r['attributes']['short_name'])
    print("\n")
    #directions = rt.get(id='Red')['data'][0]['attributes']['direction_destinations']

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
