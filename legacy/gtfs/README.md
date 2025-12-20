# mbta-gtfs
Visualize mbta info using gtfs and gtfs-realtime data from MBTA (not V3_API)

Requires: pandas, geopy, gtfs-realtime-bindings

Refer to individual scripts for details. 

mbta_stop_id.py requires the gtfs feed from MBTA to be downloaded from:

https://cdn.mbta.com/MBTA_GTFS.zip

The file must be unzipped in the same folder as the py scripts. 

Wheel packages: prepare it using `python -m build` in each of the folders. Install wheel using pip.

