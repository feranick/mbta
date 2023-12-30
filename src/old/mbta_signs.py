from pymbta3 import Stops, Predictions
from datetime import datetime
import time

key = "91944a70800a4bcabe1b9c2023d12fc8"

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)
    
def get_dir(a):
    if a == 0:
        return "Ashmont/Braintree"
    else:
        return "Alewife"

st = Stops(key=key)
stops = st.get(route='Red')['data']
#stops = st.get(route='Red')['data']
lo = []
la = []
stats = ['place-knncl', 'place-chmnl']
for s in stops:
    if s['id'] in stats:
        #print(s)
        #print(s['attributes']['latitude'])
        #print(s['attributes']['longitude'])
        la.append(s['attributes']['latitude'])
        lo.append(s['attributes']['longitude'])
        
print("\n")
        
pr = Predictions(key=key)

while True:
    pred = pr.get(longitude=lo[0], latitude=la[0], radius=0.001)['data']
    dummy = 0
    pred_arr_times = []
    for p in pred:
        if p['relationships']['route']['data']['id'] == 'Red' and dummy < 4:
        
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            arr_time = p['attributes']['arrival_time'][11:][:8]
            dep_time = p['attributes']['departure_time'][11:][:8]
            arr_time_mins = round((get_sec(arr_time) - get_sec(current_time))/60)
            dep_time_mins = round((get_sec(dep_time) - get_sec(current_time))/60)
            pred_arr_times.append(arr_time_mins)
            dummy += 1
      
    if pred_arr_times[0] > 0 and pred_arr_times[0] < 1:
        print(get_dir(p['attributes']['direction_id']), "ARR")
    if pred_arr_times[0] >= 1:
        print(get_dir(p['attributes']['direction_id']), pred_arr_times[0],"MINS")
    if pred_arr_times[0] <=0:
        print(get_dir(p['attributes']['direction_id']), " NOW BOARD")
        
    print(get_dir(p['attributes']['direction_id']), pred_arr_times[1],"MINS")
    print("\n")
    
    time.sleep(10)
            

