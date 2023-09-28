import math
from machine import Pin
from neopixel import Neopixel

#######################################################################
# Pins

PIN_STRIP_0 = 0
PIN_STRIP_1 = 1
PIN_STRIP_2 = 2
PIN_STRIP_3 = 3
PIN_STRIP_4 = 4
PIN_STRIP_5 = 5
PIN_STRIP_6 = 6
PIN_STRIP_7 = 7
PIN_STRIP_8 = 8
PIN_STRIP_9 = 9
PIN_STRIP_10 = 10
PIN_STRIP_11 = 11

#######################################################################
# Constants

WIDTH = 12
HEIGHT = 5

COLOR_ON_RGB = (255,0,0)
COLOR_OFF_RGB = (0,0,0)

MIN_HUE = 30000
MAX_HUE = 65535


#######################################################################
# Neopixel init

strips = [
    Neopixel(HEIGHT, 0, PIN_STRIP_0, "GRB"),
    Neopixel(HEIGHT, 1, PIN_STRIP_1, "GRB"),
    Neopixel(HEIGHT, 2, PIN_STRIP_2, "GRB"),
    Neopixel(HEIGHT, 3, PIN_STRIP_3, "GRB"),
    Neopixel(HEIGHT, 4, PIN_STRIP_4, "GRB"),
    Neopixel(HEIGHT, 5, PIN_STRIP_5, "GRB"),
    Neopixel(HEIGHT, 6, PIN_STRIP_6, "GRB"),
    Neopixel(HEIGHT, 7, PIN_STRIP_7, "GRB"),
    Neopixel(HEIGHT, 0, PIN_STRIP_8, "GRB"),
    Neopixel(HEIGHT, 2, PIN_STRIP_9, "GRB"),
    Neopixel(HEIGHT, 3, PIN_STRIP_10, "GRB"),
    Neopixel(HEIGHT, 4, PIN_STRIP_11, "GRB"),
]

def updatePixelHsv(x, y, colorHsv):
    h,s,v = colorHsv
    strips[x].set_pixel(y, strips[x].colorHSV(h,s,v))

def updatePixelRgb(x, y, colorRbg):
    strips[x].set_pixel(y, colorRbg)

def show():

    for stripIndex in range(WIDTH):
        print('stripIndex', stripIndex)
        strips[stripIndex].show()

updatePixelHsv(0, 0, (0,255,255))
show()

updatePixelHsv(0, 2, (0,0,0))
show()

updatePixelHsv(11, 0, (0,255,255))
show()

updatePixelHsv(5, 0, (0,255,255))
show()

updatePixelHsv(0, 0, (0,0,0))
show()