from pymbta3 import Stops, Vehicles

key = "91944a70800a4bcabe1b9c2023d12fc8"

line = "Orange"
line = "Red"
line = "Blue"

st = Stops(key=key)
stops = st.get(route=line)['data']
#stops = st.get(id=station)['data']

for s in stops:
    print(s)
    print(s['id'],s['attributes']['name'])


