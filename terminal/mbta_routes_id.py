#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************
* MBTA ROUTES ID
* v2024.01.03.1
* By: Nicola Ferralis <feranick@hotmail.com>
**********************************************
'''
#print(__doc__)

from pymbta3 import Routes

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
    rt = Routes(key=dP.key)
    #routes = rt.get(id='Red')['data']
    #for r in routes:
    #    print(r)
    
    routes = rt.get(type=type)['data']
    print("\nID, short_name")
    for r in routes:
        print(r['id'], r['attributes']['short_name'])
    print("\n")
    #directions = rt.get(id='Red')['data'][0]['attributes']['direction_destinations']

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
