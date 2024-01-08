# mbta
Visualize mbta times/info via TFT screen on a Raspberry Pi

Display: https://learn.adafruit.com/adafruit-1-9-color-ips-tft-display

Refer to individual scripts for details. 

Set up Blinka:
`sudo pip3 install --upgrade adafruit-python-shell`
`wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py`
`sudo -E env PATH=$PATH python3 raspi-blinka.py`


Requires adafruit-circuitpython-rgb-display, adafruit-circuitpython-st7789 adafruit-circuitpython-display-text 

sudo pip3 install adafruit-circuitpython-st7789 adafruit-circuitpython-display-text
sudo apt install python3-numpy python3-pil

Wheel packages: prepare it using `python -m build` in each of the folders. Install wheel using pip.

