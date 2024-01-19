#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************
* MBTA LINES
* v2024.01.19.1
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
    
    station = sys.argv[1]
    print("Lines running through "+mk_stop_URL(station)+":\n")
    lines = []

    routes = requests.get(dP.url+"routes/?filter[stop]="+station,headers=dP.headers).json()['data']    
    for r in routes:
        lines.append(r['id'])
    
    print(" ".join(lines))
    print("\n")


def mk_line_URL(line):
    return "<a href=\"https://mbta.com/schedules/"+line+"/line\" target=\"_blank\" rel=\"noopener noreferrer\">"+line+"</a>"
    
def mk_stop_URL(station):
    return "<a href=\"https://mbta.com/stops/"+station+"\" target=\"_blank\" rel=\"noopener noreferrer\">"+get_stop(station)+" ("+station+")</a>"
    
def get_stop(stop):
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
