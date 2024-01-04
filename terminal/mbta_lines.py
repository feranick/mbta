#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************
* MBTA LINES
* v2024.01.04.1
* By: Nicola Ferralis <feranick@hotmail.com>
**********************************************
'''
#print(__doc__)

#from pymbta3 import Stops, Routes
import sys, requests

#***************************************************
# This is needed for installation through pip
#***************************************************
def mbta_lines():
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
    print("\n Find which line runs through a specific station:")
    station = input()
    print("\n Searching for routes passing through:",station,"\n Please wait...\n")
    lines = []

    #st = Stops(key=dP.key)
    #rt = Routes(key=dP.key)
    #routes = rt.get()['data']
    
    routes = requests.get(dP.url+"routes/",headers=dP.headers).json()['data']
    
    for r in routes:
        #print(r['id'], r['attributes']['short_name'])
        #stops = st.get(route=r['id'])['data']
        st_url = dP.url+"stops/?filter[route]="+r['id']
        stops = requests.get(st_url,headers=dP.headers).json()['data']
        
        for s in stops:
            if s['id'] == station:
                lines.append(r['id'])
        #print(s['id'],s['attributes']['name'])
        #tmp_stops.append(s['id'])
    print(lines)
    print("\n")

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
