#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************
* GTFS VEHICLE ID
* v2024.01.05.1
* By: Nicola Ferralis <feranick@hotmail.com>
**********************************************
'''
#print(__doc__)

#from pymbta3 import Alerts
from google.protobuf.json_format import ParseDict, MessageToJson
from google.transit import gtfs_realtime_pb2
from geopy.geocoders import Nominatim
from datetime import datetime
import pandas as pd
import sys, requests

#***************************************************
# This is needed for installation through pip
#***************************************************
def gtfs_vehicle_id():
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
        self.trips_file = "trips.txt"

#************************************
''' Main '''
#************************************
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print(' Usage:\n  python3 gtfs_vehicles_id.py <vehicle_id>')
        print('  python3 gfts_vehicles.py list \n   To list MBTA fleet\n')
        return
        
    dP = Conf()
    v_feed = gtfs_realtime_pb2.FeedMessage()
    v = requests.get(dP.url_v)
    v_feed.ParseFromString(v.content)

    print("\n")
    
    if sys.argv[1] == "list":
        print()
        for entity in v_feed.entity:
            print(entity.vehicle.vehicle.label, entity.vehicle.vehicle.id,entity.vehicle.trip.route_id)
        return
        
    vehicle = sys.argv[1]
    for entity in v_feed.entity:
        if entity.vehicle.vehicle.label == vehicle:
            print(entity.vehicle)
            print(" Vehicle label:", vehicle)
            print(" Vehicle ID:",entity.vehicle.vehicle.id)
            print(" License plate:",entity.vehicle.vehicle.license_plate)
            print(" Route:",entity.vehicle.trip.route_id)
            print(" Occupancy:",occupancy(entity.vehicle),"-",str(entity.vehicle.occupancy_percentage)+"%")
            print(" Longitude:",entity.vehicle.position.longitude)
            print(" Latitude: ",entity.vehicle.position.latitude)
            print(" Bearing: ",entity.vehicle.position.bearing)
            print(" Speed:",entity.vehicle.position.speed)
            print(" Stop sequence:",entity.vehicle.current_stop_sequence)
            print(" Status:",current_status(entity.vehicle.current_status), get_station(entity.vehicle.stop_id),"(Stop ID:",entity.vehicle.stop_id+")")
            print(" Congestion level:", congestion(entity.vehicle.congestion_level))
            print(" Time:",datetime.fromtimestamp(entity.vehicle.timestamp))
            coord = str(entity.vehicle.position.latitude)+','+str(entity.vehicle.position.longitude)
            geolocator = Nominatim(user_agent="Angelo")
            location = geolocator.reverse(coord)
            print("\n",location)
            print("\n")
            
def get_station(a):
    stops = pd.read_csv(Conf().gtfs_dir+"/"+Conf().stops_file, dtype = str)
    s_ind = stops.loc[stops['stop_id'] == a].index[0]
    return stops.loc[s_ind, 'stop_name']
                
def current_status(a):
    if a == 0:
        return "Incoming at:"
    if a == 1:
        return "Stopped at:"
    if a == 2:
        return "In transit to:"

def occupancy(a):
    if a.occupancy_status == 0:
        return "Empty"
    if a.occupancy_status == 1:
        return "Many seats available"
    if a.occupancy_status == 2:
        return "Few seats available"
    if a.occupancy_status == 3:
        return "Standing room only"
    if a.occupancy_status == 4:
        return "Crushed standing room only"
    if a.occupancy_status == 5:
        return "Full"
    if a.occupancy_status == 6:
        return "Not accepting passengers"
    if a.occupancy_status == 7:
        return "No data available"
    if a.occupancy_status == 8:
        return "Not boardable"
        
def congestion(a):
    if a == 0:
        return "Unknown"
    if a == 1:
        return "Running smoothly"
    if a == 2:
        return "Stop and go"
    if a == 3:
        return "Congestion"
    if a == 4:
        return "Severe congestion"
    
#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
