from pymbta3 import Alerts, Routes, Stops, Vehicles, Predictions, Schedules, Trips, Facilities

key = "91944a70800a4bcabe1b9c2023d12fc8"
        
# Find all Route data for the Red Line
rt = Routes(key=key)
routes = rt.get(id='Red')['data']
for r in routes:
    print(r)
    
directions = rt.get(id='Red')['data'][0]['attributes']['direction_destinations']
