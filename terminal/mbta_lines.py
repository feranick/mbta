#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************
* MBTA LINES
* v2024.01.03.1
* By: Nicola Ferralis <feranick@hotmail.com>
**********************************************
'''
#print(__doc__)

from pymbta3 import Stops, Routes
import sys

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
        self.key = "91944a70800a4bcabe1b9c2023d12fc8"

#************************************
''' Main '''
#************************************
def main():
    dP = Conf()
    print("\n Find which line runs through a specific station:")
    station = input()

    st = Stops(key=dP.key)
    rt = Routes(key=dP.key)

    print("\n Searching for routes passing through:",station,"\n Please wait...\n")
    lines = []
    routes = rt.get()['data']
    
    for r in routes:
        #print(r['id'], r['attributes']['short_name'])
        stops = st.get(route=r['id'])['data']
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
