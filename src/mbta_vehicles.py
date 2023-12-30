from pymbta3 import Alerts, Routes, Stops, Vehicles, Predictions, Schedules, Trips, Facilities
from geopy.geocoders import Nominatim

key = "91944a70800a4bcabe1b9c2023d12fc8"

vh = Vehicles(key=key)
vehicles = vh.get()['data']
for v in vehicles:
    #print(v['relationships']['route']['data']['id'])
    if v['relationships']['route']['data']['id'] == 'Red':
        print(v['attributes']['bearing'])
        print(v['attributes']['current_status'])
        print(v['attributes']['current_stop_sequence'])
        print(v['attributes']['latitude'])
        print(v['attributes']['longitude'])
        print(v['attributes']['speed'])
        geolocator = Nominatim(user_agent="Angelo")
        location = geolocator.reverse(v['attributes']['latitude'], v['attributes']['longitude'])
        print(location.address)
        print("\n")
