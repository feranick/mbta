#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************
* GTFS-realtime
* v2024.01.04.1
* By: Nicola Ferralis <feranick@hotmail.com>
**********************************************
'''
#print(__doc__)

#from pymbta3 import Alerts
from google.protobuf.json_format import ParseDict, MessageToJson
from google.transit import gtfs_realtime_pb2
from geopy.geocoders import Nominatim
from datetime import datetime
import sys, requests

#***************************************************
# This is needed for installation through pip
#***************************************************
def gtfs():
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

#************************************
''' Main '''
#************************************
def main():
    if len(sys.argv) < 1:
        print(' Usage:\n  python3 gfts_vehicles.py <vehicle_id>')
        return
        
    dP = Conf()
    vehicle = sys.argv[1]
    v_feed = gtfs_realtime_pb2.FeedMessage()
    v = requests.get(dP.url_v)
    v_feed.ParseFromString(v.content)

    #for entity in v_feed.entity:
    #    print(entity.vehicle.current_status, entity.vehicle.vehicle.label)

    for entity in v_feed.entity:
        if entity.vehicle.vehicle.label == vehicle:
            print("\n Vehicle id:", vehicle)
            print(" Occupancy:", entity.vehicle.occupancy_percentage,"%")
            print(" Longitude:",entity.vehicle.position.longitude)
            print(" Latitude: ",entity.vehicle.position.latitude)
            print(" Bearing: ",entity.vehicle.position.bearing)
            print(" Speed:",entity.vehicle.position.speed)
            print(" Stop sequence:",entity.vehicle.current_stop_sequence)
            if entity.vehicle.current_status == 0:
                status = " Incoming at:"
            if entity.vehicle.current_status == 1:
                status = " Stopped at:"
            if entity.vehicle.current_status == 2:
                status = " In transit to:"
            print(status, entity.vehicle.stop_id)
            print(" Time:",datetime.fromtimestamp(entity.vehicle.timestamp))
            
            coord = str(entity.vehicle.position.latitude)+','+str(entity.vehicle.position.longitude)
            geolocator = Nominatim(user_agent="Angelo")
            location = geolocator.reverse(coord)
            print("\n",location)
            print("\n")
                
#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
