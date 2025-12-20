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
        self.url_tu = "https://cdn.mbta.com/realtime/TripUpdates.pb"
        self.url_v = "https://cdn.mbta.com/realtime/VehiclePositions.pb"

#************************************
''' Main '''
#************************************
def main():
    dP = Conf()

    tu_feed = gtfs_realtime_pb2.FeedMessage()
    trip_updates = requests.get(dP.url_tu)
    tu_feed.ParseFromString(trip_updates.content)
    
    v_feed = gtfs_realtime_pb2.FeedMessage()
    v = requests.get(dP.url_v)
    v_feed.ParseFromString(v.content)

    #for entity in feed.entity:
    #    print(entity)
    
    #print(len(tu_feed.entity))
    #for entity in tu_feed.entity:
    #    if entity.HasField('trip_update'):
    #        print(entity.trip_update)
    #for entity in tu_feed.entity:
    #   if entity.stop_sequence == 20:
    #        entity.trip_update
    
    #for entity in tu_feed.entity:
    #   if entity.stop_sequence == 20:
    #        if entity.HasField('trip_update'):
    #            print(entity.trip_update.trip)
    
    #for entity in tu_feed.entity:
    #   if entity.stop_sequence == 20:
    #        if entity.HasField('trip_update'):
    #            dt = datetime.fromtimestamp(entity.trip_update.timestamp)
    #            print(dt)
            
    
    for entity in v_feed.entity:
        print(entity.vehicle.current_status, entity.vehicle.vehicle.label)

    for entity in v_feed.entity:
        if entity.vehicle.vehicle.label == "0784":
            print(entity)
            print(entity.vehicle.position.longitude)
            print(entity.vehicle.position.latitude)
            print(entity.vehicle.current_status, entity.vehicle.stop_id)
            print(datetime.fromtimestamp(entity.vehicle.timestamp))
    
    #print(feed.entity[0])
            

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
