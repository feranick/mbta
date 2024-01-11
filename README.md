# mbta
Visualize mbta times/info

Refer to individual scripts for details. 

Requires `pymbta3, geopy`

Three versions available: 

1. Terminal: can be run directly from the terminal
2. leds: Using a Raspberry Pi with LEDS, arrival times for a specific line at a specific station are shown via LEDs.
3. gtfs: Uses gtfs directly, not the API_v3 from MBTA. Not feature complete yet. Overall faster than APIs (both locally and in db querying), but more computationally intensive.

More to come.

Wheel packages: prepare it using `python -m build` in each of the folders. Install wheel using pip.

Web versions require apache2, php, libapache2-mod-php
