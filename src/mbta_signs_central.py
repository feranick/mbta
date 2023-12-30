from pymbta3 import Stops, Predictions, Routes
from datetime import datetime
import time

key = "91944a70800a4bcabe1b9c2023d12fc8"

station = 'place-cntsq'
#station = 'place-knncl'
#station = 'place-chmnl'

refresh_time = 10

rt = Routes(key=key)
st = Stops(key=key)
pr = Predictions(key=key)

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)
    
def get_dir(a):
    return rt.get(id='Red')['data'][0]['attributes']['direction_destinations'][a]

def arr_sign(a, b, c):
    if a > 0 and a < 1:
        print(b,"\tARR\t", c)
    if a >= 1:
        print(b,"\t",a,"min\t",c)
    if a<= 0:
        print(b,"\t NOW BOARD\t",c)

stops = st.get(route='Red')['data']
for s in stops:
    if s['id'] == station:
        la = s['attributes']['latitude']
        lo = s['attributes']['longitude']
        name = s['attributes']['name']
print("\n")
        
while True:
    pred = pr.get(longitude=lo, latitude=la, radius=0.001)['data']
    dummy = 0
    pred_arr_times = []
    direction = []
    status = []
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
            status.append(p['attributes']['status'])
            #print(p['attributes']['stop_sequence'])
            #print(p['relationships']['vehicle'])
            dummy += 1
    
    print(name,status[0])
    
    arr_sign(pred_arr_times[0], direction[0], current_time)
        
    for j in range(1,len(direction)):
        arr_sign(pred_arr_times[j], direction[j], '')
    print("\n")
    
    time.sleep(refresh_time)
            

