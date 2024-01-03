#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pymbta3 import Alerts, Routes, Stops, Vehicles, Predictions, Schedules, Trips, Facilities

key = "91944a70800a4bcabe1b9c2023d12fc8"

print("\n Type:")
print("  0	Light Rail	Green Line")
print("  1	Heavy Rail	Red Line")
print("  2	Commuter Rail")
print("  3	Bus")
print("  4	Ferry")
print("\n Use mbta_stops.py for codes of stops for a given route")
print("\n Input router type:")

station = input()

# Find all Route data for the Red Line
rt = Routes(key=key)
st = Stops(key=key)
#routes = rt.get(id='Red')['data']
#for r in routes:
#    print(r)

lines = []
    
routes = rt.get()['data']
print("\nID, short_name")
for r in routes:
    #print(r['id'], r['attributes']['short_name'])
    print(r['id'])
    stops = st.get(route=r['id'])['data']['id']
    print(stops)
    if station in stops:
        lines.append(r['id'])
    
print(lines)
print("\n")



    
#directions = rt.get(id='Red')['data'][0]['attributes']['direction_destinations']
