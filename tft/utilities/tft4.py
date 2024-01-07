# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""
import board
import terminalio
import displayio
import time

# Starting in CircuitPython 9.x fourwire will be a seperate internal library
# rather than a component of the displayio library
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire
from adafruit_display_text import label
from adafruit_st7789 import ST7789

BORDER_WIDTH = 20
TEXT_SCALE = 2

# Release any resources currently in use for the displays
displayio.release_displays()

spi = board.SPI()
tft_cs = board.CE0
tft_dc = board.D25
tft_rst = board.D24

display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)

display = ST7789(display_bus, width=320, height=170, colstart=35, rotation=90)

# Make the display context
splash = displayio.Group()
display.root_group = splash

'''
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
#color_palette[0] = 0x00FF00  # Bright Green
color_palette[0] = 0x000000  # Bright Green
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)
'''

# Draw a label
text_area = label.Label(
    terminalio.FONT,
    text="Ciao Matteo",
    color=0xFF8B00,
    scale=TEXT_SCALE,
    anchor_point=(0, 0),
    #anchored_position=(display.width // 2, display.height // 2),
    anchored_position=(0, 0),
)
splash.append(text_area)
time.sleep(2)

print("\n Should erase now.")
for i in range(len(splash)):
    print(len(splash))
    print(splash[i])
    splash.remove(splash[i])
    print(len(splash))
print("\n Erased?")


while True:
    pass
