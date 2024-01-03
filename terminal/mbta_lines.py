#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pymbta3 import Stops, Routes

key = "91944a70800a4bcabe1b9c2023d12fc8"

print("\n Find which line runs through a specific station:")
station = input()

st = Stops(key=key)
rt = Routes(key=key)

lines = []
routes = rt.get()['data']
for r in routes:
    #print(r['id'], r['attributes']['short_name'])
    print(r['id'])
    stops = st.get(route=r['id'])['data']
    for s in stops:
        if s['id'] == station:
            lines.append(r['id'])
    #print(s['id'],s['attributes']['name'])
    #tmp_stops.append(s['id'])
print(lines)
print("\n")

