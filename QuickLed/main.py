from machine import Pin
import time
from neopixel import Neopixel
from rotary_encoder import RotaryEncoder
import math

#######################################################################
# Pins

ROTARY_CLK = 0
ROTARY_DT = 1

STRIP_PIN = 2

#######################################################################
# Constants

MIN_HUE = 0
MAX_HUE = 65535

HUE_INC = math.floor(MAX_HUE / 30)

#######################################################################
# Global variables

hue = MIN_HUE

#######################################################################
# Strip init

NUM_LEDS = 9
STATE_MACHINE = 0

strip = Neopixel(
    NUM_LEDS,
    STATE_MACHINE,
    STRIP_PIN,
    "GRB"
)

def updateStrip():
    strip.fill(strip.colorHSV(hue, 255, 100))
    strip.show()

#######################################################################
# Rotary encoder init

def onRotate(clockwise):
    global hue
    if clockwise:
        if hue < MAX_HUE:
            hue += HUE_INC
        else:
            hue = MIN_HUE
    else:
        if hue > MIN_HUE:
            hue -= HUE_INC
        else:
            hue = MAX_HUE

    print('hue', hue)
    updateStrip()

rotary = RotaryEncoder(
    Pin(ROTARY_CLK, Pin.IN, Pin.PULL_UP),
    Pin(ROTARY_DT, Pin.IN, Pin.PULL_UP),
    onRotate
)

#######################################################################
# Main program

updateStrip()

while True:
    rotary.listenToRotation()