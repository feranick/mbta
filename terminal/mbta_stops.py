#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************
* MBTA STOPS
* v2024.01.03.1
* By: Nicola Ferralis <feranick@hotmail.com>
**********************************************
'''
#print(__doc__)
from pymbta3 import Stops, Vehicles

#************************************
''' Params '''
#************************************
class Conf:
    key = "91944a70800a4bcabe1b9c2023d12fc8"

#************************************
''' Main '''
#************************************
def main():
    dP.Conf()
    print("\n Line:")
    print("  Orange")
    print("  Red")
    print("  Blue")
    print("  1 or 741 for SL1 or 747 for CT2")
    print("  CR-Providence")
    print("  Green-E - Medford")
    print("  Green-D - Somerville")
    print("\n Use mbta_routes_id.py for all routes")
    print("\n Input line:")

    line = input()
    st = Stops(key=dP.key)
    stops = st.get(route=line)['data']
    #stops = st.get(id=station)['data']

    print("\nID, name")
    for s in stops:
        #print(s)
        print(s['id'],s['attributes']['name'])
    print("\n")
    
#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())


