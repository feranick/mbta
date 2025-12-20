#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************
* MBTA STOPS
* v2024.01.10.1
* By: Nicola Ferralis <feranick@hotmail.com>
**********************************************
'''
#print(__doc__)

#from pymbta3 import Stops, Vehicles
import sys, requests

#***************************************************
# This is needed for installation through pip
#***************************************************
def mbta_stops():
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
    
    st_url = dP.url+"stops/?filter[route]="+sys.argv[1]
    stops = requests.get(st_url,headers=dP.headers).json()['data']

    print("\n ID, name")
    for s in stops:
        #print(s)
        print(" ",s['id'],s['attributes']['name'])
    print("\n")
    
#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())


