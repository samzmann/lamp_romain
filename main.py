from machine import Pin
import time
from neopixel import Neopixel
from rotary_encoder import RotaryEncoder
import math

#######################################################################
# Strip init

NUM_LEDS = 9
STATE_MACHINE = 0
STRIP_PIN = 6

strip = Neopixel(
    NUM_LEDS,
    STATE_MACHINE,
    STRIP_PIN,
    "GRB"
)

ledOnIndex = -1

MIN_INDEX = -1
MAX_INDEX = NUM_LEDS - 1


MIN_HUE = 0
MAX_HUE = 65535

MIN_HUE_WIDTH = 0
HUE_WIDTH_STEP = math.floor(MAX_HUE / NUM_LEDS)
MAX_HUE_WIDTH = HUE_WIDTH_STEP * NUM_LEDS
hueWidth = MAX_HUE_WIDTH / 3

startHue = 0
endHue = startHue + hueWidth

START_HUE_STEP = math.floor(MAX_HUE / NUM_LEDS)

hue = startHue

#######################################################################
# Rotary encoder init

def onR1Clockwise():
    global ledOnIndex

    print('r1 clockwise')
    if ledOnIndex < MAX_INDEX:
        ledOnIndex += 1

def onR1AntiClockwise():
    global ledOnIndex
    global hue

    print('r1 anti clockwise')
    if ledOnIndex > MIN_INDEX:
        ledOnIndex -= 1

r1 = RotaryEncoder(
    Pin(4, Pin.IN, Pin.PULL_UP),
    Pin(5, Pin.IN, Pin.PULL_UP),
    onR1Clockwise,
    onR1AntiClockwise
)

def onR2Clockwise():
    global startHue

    print('r2 clockwise')

    # if startHue < MAX_HUE_WIDTH:
    startHue += START_HUE_STEP
    print('startHue',startHue)

def onR2AntiClockwise():
    global startHue

    print('r2 anti clockwise')

    # if startHue > MIN_HUE_WIDTH:
    startHue -= START_HUE_STEP
    print('startHue',startHue)

r2 = RotaryEncoder(
    Pin(2, Pin.IN, Pin.PULL_UP),
    Pin(3, Pin.IN, Pin.PULL_UP),
    onR2Clockwise,
    onR2AntiClockwise
)

def onR3Clockwise():
    global hueWidth
    print('r3 clockwise')

    if hueWidth < MAX_HUE_WIDTH:
        hueWidth += HUE_WIDTH_STEP
        print('hueWidth',hueWidth)


def onR3AntiClockwise():
    global hueWidth
    print('r3 anti clockwise')

    if hueWidth > MIN_HUE_WIDTH:
        hueWidth -= HUE_WIDTH_STEP
        print('hueWidth',hueWidth)

r3 = RotaryEncoder(
    Pin(0, Pin.IN, Pin.PULL_UP),
    Pin(1, Pin.IN, Pin.PULL_UP),
    onR3Clockwise,
    onR3AntiClockwise
)

#######################################################################

def updateStrip():
    strip.brightness(255)
    
    h = startHue

    for ledIndex in range(NUM_LEDS):
        if ledIndex <= ledOnIndex:
            strip.set_pixel(ledIndex, strip.colorHSV(h, 255, 255))
        else:
            strip.set_pixel(ledIndex, strip.colorHSV(h, 255, 0))
        
        h += math.floor(hueWidth)
    
    
    strip.show()
    
    
while True:
   r1.rotaryChanged()
   r2.rotaryChanged()
   r3.rotaryChanged()
   updateStrip()



