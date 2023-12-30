from pymbta3 import Stops, Predictions, Routes, Vehicles
from datetime import datetime
import time

key = "91944a70800a4bcabe1b9c2023d12fc8"

station = 'place-cntsq'
#station = 'place-knncl'
#station = 'place-chmnl'
line = 'Red'

refresh_time = 10

rt = Routes(key=key)
st = Stops(key=key)
pr = Predictions(key=key)
vh = Vehicles(key=key)

########################
# Definitions
########################
def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)
    
def get_dir(a):
    return rt.get(id=line)['data'][0]['attributes']['direction_destinations'][a]

def arr_sign(a, b, st, station):
    if a > 0 and a < 1:
        print(b,"\tARR\t\t", st, station)
    if a >= 1:
        print(b,"\t",a,"min\t\t", st, station)
    if a<= 0:
        print(b,"\t NOW BOARD\t\t", st, station)

def get_stat(la, lo):
    s = st.get(route='line', longitude=lo, latitude=la, radius=0.005)['data']
    if len(s) == 0:
        return ''
    else:
        return s[0]['attributes']['name']

############################
# get coord/name station
############################
s = st.get(route=line, id=station)['data'][0]['attributes']
la = s['latitude']
lo = s['longitude']
name = s['name']
print("\n")

############################
# Loop
############################
while True:
    pred = pr.get(longitude=lo, latitude=la, radius=0.001)['data']
    dummy = 0
    pred_arr_times = []
    direction = []
    status = []
    vstation = []
    vstatus = []
    
    for p in pred:
        if p['relationships']['route']['data']['id'] == line and dummy < 6:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            arr_time = p['attributes']['arrival_time'][11:][:8]
            dep_time = p['attributes']['departure_time'][11:][:8]
            arr_time_mins = round((get_sec(arr_time) - get_sec(current_time))/60)
            dep_time_mins = round((get_sec(dep_time) - get_sec(current_time))/60)
            pred_arr_times.append(arr_time_mins)
            direction.append(get_dir(p['attributes']['direction_id']))
            status.append(p['attributes']['status'])
            v = vh.get(id=p['relationships']['vehicle']['data']['id'])['data'][0]['attributes']
            vstatus.append(v['current_status'])
            vstation.append(get_stat(v['latitude'], v['longitude']))
            dummy += 1
            
    print(name,"\t\t",current_time)
    arr_sign(pred_arr_times[0], direction[0], vstatus[0], vstation[0])
        
    for j in range(1,len(direction)):
        arr_sign(pred_arr_times[j], direction[j], vstatus[j], vstation[j])
    print("\n")
    
    time.sleep(refresh_time)
            

