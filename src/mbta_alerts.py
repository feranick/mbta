#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pymbta3 import Alerts, Routes, Stops, Vehicles, Predictions, Schedules, Trips, Facilities
from datetime import datetime

key = "91944a70800a4bcabe1b9c2023d12fc8"


at = Alerts(key=key)
#alerts = at.get(stop='place-alfcl')['data']
alerts = at.get(route=['Red'])['data']
for alert in alerts:
    print(alert['attributes']['short_header'])
    #print(alert['attributes']['header'])
    print(alert['attributes']['informed_entity'])
        
