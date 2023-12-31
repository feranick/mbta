from pymbta3 import Alerts, Routes, Stops, Vehicles, Predictions, Schedules, Trips, Facilities
from datetime import datetime
from geopy.geocoders import Nominatim

key = "91944a70800a4bcabe1b9c2023d12fc8"

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)
    
def get_dir(a):
    if a == 0:
        return "Alewife"
    else:
        return "Ashmont/Braintree"

st = Stops(key=key)
stops = st.get(route='Red')['data']
#stops = st.get(route='Red')['data']
lo = []
la = []
stats = ['place-knncl', 'place-chmnl']
for s in stops:
    if s['id'] in stats:
        #print(s)
        print(s['attributes']['latitude'])
        print(s['attributes']['longitude'])
        la.append(s['attributes']['latitude'])
        lo.append(s['attributes']['longitude'])
        
pr = Predictions(key=key)
for i in [0,1]:
    pred = pr.get(longitude=lo[i], latitude=la[i], radius=0.001)['data']
    #pred = pr.get(longitude=-71.086176, latitude=42.362491, radius=0.001)['data']
    print(stats[i])
    dummy = 0
    for p in pred:
        if p['relationships']['route']['data']['id'] == 'Red' and dummy < 4:
            print(stats[i],lo[i],la[i])
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)
            print(get_sec(current_time))
            
            arr_time = p['attributes']['arrival_time'][11:][:8]
            dep_time = p['attributes']['departure_time'][11:][:8]
            
            arr_time_mins = round((get_sec(arr_time) - get_sec(current_time))/60)
            dep_time_mins = round((get_sec(dep_time) - get_sec(current_time))/60)
            
            print('ARR TIME:',arr_time)
            print('ARR TIME MINS:',arr_time_mins)
            #print('ARR UNC:',p['attributes']['arrival_uncertainty'])
            print('DEP TIME:',dep_time)
            print('DEP TIME MINS:',dep_time_mins)
            
            
            #print('DEP UNC:',p['attributes']['arrival_uncertainty'])
            print('DIR:',get_dir(p['attributes']['direction_id']))
            print("\n")
            dummy += 1
            
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

#at = Alerts(key=key)
#alerts = at.get(stop='place-alfcl')['data']
#alerts = at.get(route=['Red'])['data']
#for alert in alerts:
#    print(alert['attributes']['short_header'])
#    #print(alert['attributes']['header'])
#    print(alert['attributes']['informed_entity'])
        
# Find all Route data for the Red Line
#rt = Routes(key=key)
#routes = rt.get(id='Red')['data']
#for r in routes:
#    print(r)

#vh = Vehicles(key=key)
#vehicles = vh.get()['data']
#for v in vehicles:
#    #print(v['relationships']['route']['data']['id'])
#    if v['relationships']['route']['data']['id'] == 'Red':
#        print(v['attributes']['bearing'])
#        print(v['attributes']['current_status'])
#        print(v['attributes']['current_stop_sequence'])
#        print(v['attributes']['latitude'])
#        print(v['attributes']['longitude'])
#        print(v['attributes']['speed'])
#        geolocator = Nominatim(user_agent="Angelo")
#        location = geolocator.reverse(v['attributes']['latitude'], v['attributes']['longitude'])
#        print(location.address)
#        print("\n")
