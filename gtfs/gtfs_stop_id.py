#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************
* GTFS STOP ID
* v2024.01.05.1
* By: Nicola Ferralis <feranick@hotmail.com>
**********************************************
'''
#print(__doc__)

#from pymbta3 import Alerts
from google.protobuf.json_format import ParseDict, MessageToJson
from google.transit import gtfs_realtime_pb2
import pandas as pd
from datetime import datetime
import sys, requests

#***************************************************
# This is needed for installation through pip
#***************************************************
def gtfs_stop_id():
    main()

#************************************
''' Params '''
#************************************
class Conf:
    def __init__(self):
        #self.url = "https://api.bart.gov/gtfsrt/tripupdate.aspx"
        #self.url = "https://cdn.mbta.com/realtime/Alerts.pb"
        #self.url_tu = "https://cdn.mbta.com/realtime/TripUpdates.pb"
        self.url_v = "https://cdn.mbta.com/realtime/VehiclePositions.pb"
        self.gtfs_dir = "MBTA_GTFS"
        self.stops_file = "stops.txt"
        self.stop_times_file = "stop_times.txt"
        self.trips_file = "trips.txt"

#************************************
''' Main '''
#************************************
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print(' Usage:\n  python3 gtfs_stop_id.py <stop_id>')
        print('  python3 gfts_vehicles.py list \n   To list MBTA fleet\n')
        return
        
    dP = Conf()
    stops = pd.read_csv(dP.gtfs_dir+"/"+dP.stops_file, dtype = str)
    s_ind = stops.loc[stops['stop_id'] == sys.argv[1]].index[0]
        
    print("\n Stop ID:", sys.argv[1])
    print(" Stop name:",stops.loc[s_ind, 'stop_name'])
    print(" On street:",stops.loc[s_ind, 'on_street'])
    print(" At street:",stops.loc[s_ind, 'at_street'])
    print(" Address:",stops.loc[s_ind, 'stop_address'])
    print(" Municipality:",stops.loc[s_ind, 'municipality'])
    print(" Latitude:",stops.loc[s_ind, 'stop_lat'])
    print(" Longitude:",stops.loc[s_ind, 'stop_lon'])
    print(" Wheelchair:",get_wheelchair(stops.loc[s_ind, 'wheelchair_boarding']))
    print(" Vehicle type:",get_vehicle_type(stops.loc[s_ind, 'vehicle_type']))
    print(" Stop URL:",stops.loc[s_ind, 'stop_url'])
    print(" Routes through station:"," ".join(find_routes_through_station(dP, sys.argv[1])))
    print("\n")
    
def find_routes_through_station(dP, a):
    stimes = pd.read_csv(dP.gtfs_dir+"/"+dP.stop_times_file, dtype = str)
    st = []
    if a.isdigit():
        st = stimes[stimes['stop_id'] == a]['trip_id'].unique().tolist()
    else:
        st = stimes[stimes['checkpoint_id'].str.contains(a[6:], na=False, regex=True)]['trip_id'].unique().tolist()

    trips = pd.read_csv(dP.gtfs_dir+"/"+dP.trips_file, dtype = str)
    return trips[trips['trip_id'].isin(st)]['route_id'].unique()

    
def get_wheelchair(a):
    if a == 0:
        return "No info"
    if a == 1:
        return "Some access"
    if a == 1:
        return "No access"
        
def get_loc_type(a):
    if a == 0 or a == None:
        return "Stop"
    if a == 1:
        return "Station"
    if a == 2:
        return "Entrance/Exit"
    if a == 3:
        return "Generic Node"
    if a == 4:
        return "Boarding Area"

def get_vehicle_type(a):
    if a == 0:
        return "Light Rail (Green Line)"
    if a == 1:
        return "Heavy Rail (Red/Orange Lines)"
    if a == 2:
        return "Commuter Rail"
    if a == 3:
        return "Bus"
    if a == 4:
        return "Ferry"
    
#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
