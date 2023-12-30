from pymbta3 import Stops, Predictions, Routes
from datetime import datetime
import time

key = "91944a70800a4bcabe1b9c2023d12fc8"

station = 'place-cntsq'
#station = 'place-knncl'
#station = 'place-chmnl'

rt = Routes(key=key)

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)
    
def get_dir(a):
    #if a == 0:
    #    return "Ashmont/Braintree"
    #else:
    #    return "Alewife"
    return rt.get(id='Red')['data'][0]['attributes']['direction_destinations'][a]

st = Stops(key=key)
stops = st.get(route='Red')['data']

for s in stops:
    if s['id'] == station:
        la = s['attributes']['latitude']
        lo = s['attributes']['longitude']
        name = s['attributes']['name']
print("\n")
        
pr = Predictions(key=key)

while True:
    pred = pr.get(longitude=lo, latitude=la, radius=0.001)['data']
    dummy = 0
    pred_arr_times = []
    direction = []
    for p in pred:
        if p['relationships']['route']['data']['id'] == 'Red' and dummy < 6:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            arr_time = p['attributes']['arrival_time'][11:][:8]
            dep_time = p['attributes']['departure_time'][11:][:8]
            arr_time_mins = round((get_sec(arr_time) - get_sec(current_time))/60)
            dep_time_mins = round((get_sec(dep_time) - get_sec(current_time))/60)
            pred_arr_times.append(arr_time_mins)
            direction.append(get_dir(p['attributes']['direction_id']))
            dummy += 1
    
    print(name)
    if pred_arr_times[0] > 0 and pred_arr_times[0] < 1:
        print(direction[0],"\tARR\t", current_time)
    if pred_arr_times[0] >= 1:
        print(direction[0],"\t",pred_arr_times[0],"min\t",current_time)
    if pred_arr_times[0] <= 0:
        print(direction[0],"\t NOW BOARD\t",current_time)
    
    for j in range(1,len(direction)):
        print(direction[j],"\t",pred_arr_times[j],"min")
    print("\n")
    
    time.sleep(10)
            

