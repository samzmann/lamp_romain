from machine import Pin
import time
from neopixel import Neopixel
import math

NUM_LEDS = 10
STATE_MACHINE = 0
STRIP_PIN = 5

strip = Neopixel(
    NUM_LEDS,
    STATE_MACHINE,
    STRIP_PIN,
    "GRB"
)


CLK_PIN = Pin(0, Pin.IN, Pin.PULL_UP)
DT_PIN = Pin(1, Pin.IN, Pin.PULL_UP)

prevRotaryVal = CLK_PIN.value()

prevTimestamp = 0

ledOnIndex = -1

MIN_INDEX = -1
MAX_INDEX = NUM_LEDS - 1



START_HUE = 20000
END_HUE = 0

HUE_STEP = math.floor(START_HUE / NUM_LEDS)

hue = START_HUE

def rotaryChanged():
    global prevRotaryVal
    global ledOnIndex
    global hue
    
    val = CLK_PIN.value()
    
    
    if val != prevRotaryVal:
    
        
        if DT_PIN.value() == val:
            print("anti-clockwise")
            if ledOnIndex > MIN_INDEX:
                ledOnIndex -= 1
                hue += HUE_STEP
                print('ledOnIndex', ledOnIndex)
                
            
        else:
            print("clockwise")
            if ledOnIndex < MAX_INDEX:
                ledOnIndex += 1
                hue -= HUE_STEP
                print('ledOnIndex', ledOnIndex)
            
        prevRotaryVal = val

def updateStrip():
    strip.brightness(50)
    
    for ledIndex in range(NUM_LEDS):
        if ledIndex <= ledOnIndex:
            strip.set_pixel(ledIndex, strip.colorHSV(hue, 255, 255))
        else:
            strip.set_pixel(ledIndex, strip.colorHSV(hue, 255, 0))
    
    
    strip.show()
    
    
while True:
   rotaryChanged()
   updateStrip()



