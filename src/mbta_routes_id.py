#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pymbta3 import Alerts, Routes, Stops, Vehicles, Predictions, Schedules, Trips, Facilities

key = "91944a70800a4bcabe1b9c2023d12fc8"
        
# Find all Route data for the Red Line
rt = Routes(key=key)
#routes = rt.get(id='Red')['data']
#for r in routes:
#    print(r)
    
routes = rt.get(type=2)['data']
for r in routes:
    print(r['id'])
    
#directions = rt.get(id='Red')['data'][0]['attributes']['direction_destinations']

''' type
0	Light Rail	Green Line
1	Heavy Rail	Red Line
2	Commuter Rail	
3	Bus	
4	Ferry	
'''
