try:
    from board_definitions.raspberry_pi_pico_w import GP10, GP11, GP16, GP17, GP18, GP0, LED
except ImportError:  # pragma: no cover
    # noinspection PyPackageRequirements
    from board import GP10, GP11, GP16, GP17, GP18, GP0, LED
from busio import SPI
from displayio import release_displays, Group, Bitmap, Palette, TileGrid
from terminalio import FONT
from fourwire import FourWire
from adafruit_display_text import label
from adafruit_st7735r import ST7735R

# Defines all the pins we use for easier access
mosi_pin = GP11
clk_pin = GP10
reset_pin = GP17
cs_pin = GP18
dc_pin = GP16

# Defines everything about the display.
# Shouldn't have to ever change much of this portion since our pinouts stay the same
release_displays()
spi = SPI(clock=clk_pin, MOSI=mosi_pin)
display_bus = FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin)
display = ST7735R(display_bus, width=128, height=160, bgr=True)
splash = Group()
display.root_group = splash

# Creates an initial large white bitmap to act as our main background color
color_bitmap = Bitmap(128, 160, 1)
color_palette = Palette(1)
color_palette[0] = [255, 255, 255]
bg_sprite = TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Creates a black rectangle just smaller than our screen's size
# This visually makes the white background we just made look like a border
inner_bitmap = Bitmap(118, 120, 1)
inner_palette = Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=35)
splash.append(inner_sprite)

# Here is the only instance (in this code) of "groups." These groups are
# basically here to make formatting easier. This code defines a new Group()
# with a scale of 2 and positions it on the screen accordingly.
# We can add as many label.Label() objects as we want to this group.
large_text_group = Group(scale=2, x=16, y=18)
large_text_area = label.Label(FONT, text="LOADING", color=0x000000)
large_text_group.append(large_text_area)
splash.append(large_text_group)