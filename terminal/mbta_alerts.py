#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************
* MBTA ALERTS
* v2024.01.04.1
* By: Nicola Ferralis <feranick@hotmail.com>
**********************************************
'''
#print(__doc__)

#from pymbta3 import Alerts
from datetime import datetime
import sys, requests

#***************************************************
# This is needed for installation through pip
#***************************************************
def mbta_alerts():
    main()
    
#************************************
''' Main '''
#************************************
def main():
    url = "https://api-v3.mbta.com/"
    key = "91944a70800a4bcabe1b9c2023d12fc8"
    headers = {'Accept': 'application/json', 'x-api-key': key}
    
    #at = Alerts(key=key)
    #alerts = at.get(stop='place-alfcl')['data']
    #alerts = at.get(route=['Red'])['data']
    
    al_url = url+"alerts/?filter[route]="+"Red+"
    alerts = requests.get(al_url,headers=headers).json()['data']
    
    for alert in alerts:
        print(alert['attributes']['short_header'])
        #print(alert['attributes']['header'])
        print(alert['attributes']['informed_entity'],"\n")
        
#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
