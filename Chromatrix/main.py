import math
from machine import Pin
from neopixel import Neopixel
from rotary_encoder import RotaryEncoder
import time
import random

def multiply_rgb(rgb, factor):
    return tuple(int(value * factor) for value in rgb)

#######################################################################
# Pins

PIN_STRIP_0 = 0
PIN_STRIP_1 = 1
PIN_STRIP_2 = 2
PIN_STRIP_3 = 3
PIN_STRIP_4 = 4

PIN_ROTARY_X_CLK = 5
PIN_ROTARY_X_DT = 6

PIN_ROTARY_Y_CLK = 7
PIN_ROTARY_Y_DT = 8

#######################################################################
# Constants

WIDTH = 5
HEIGHT = 10

COLOR_ON = (255,0,0)
COLOR_OFF = (0,0,0)

MIN_HUE = 30000
MAX_HUE = 65535

HISTORY_MIN_LENGTH = 1
HISTORY_MAX_LENGTH = 10

#######################################################################
# Global variables

posX = 0
prevPosX = posX

posY = 0
prevPosY = posY

history = [(posX, posY)]

#######################################################################
# Neopixel init

strips = [
    Neopixel(HEIGHT, 0, PIN_STRIP_0, "GRB"),
    Neopixel(HEIGHT, 1, PIN_STRIP_1, "GRB"),
    Neopixel(HEIGHT, 2, PIN_STRIP_2, "GRB"),
    Neopixel(HEIGHT, 3, PIN_STRIP_3, "GRB"),
    Neopixel(HEIGHT, 4, PIN_STRIP_4, "GRB"),
]

def updatePixel(x, y, color):

    h,s,v = color
    strips[x].set_pixel(y, strips[x].colorHSV(h,s,v))

def show():

    for stripIndex in range(WIDTH):
        strips[stripIndex].show()

def addToHistory(coordinates):
    history.append(coordinates)


def updatePosAndShow():
    global prevPosX
    global prevPosY
    
    if len(history) > HISTORY_MAX_LENGTH:
        x,y = history[0]
        updatePixel(x, y, COLOR_OFF)
        history.pop(0)

    for index in range(len(history)):
        x, y = history[index]
        hue = math.floor(MAX_HUE - MIN_HUE * (index / len(history))) + MIN_HUE
        brightness = math.floor(255 * (index / len(history)))
        color = (hue, 255, brightness)
        updatePixel(x, y, color)

    show()

#######################################################################
# Rotary encoder init

def onRotateX(clockwise):
    global posX

    if clockwise == True:
        if posX < WIDTH - 1:
            posX += 1
        else:
            posX = 0

    else:
        if posX == 0:
            posX = WIDTH - 1
        else:
            posX -= 1

    addToHistory((posX, posY))
    updatePosAndShow()

rotaryX = RotaryEncoder(
    Pin(PIN_ROTARY_X_CLK, Pin.IN, Pin.PULL_UP),
    Pin(PIN_ROTARY_X_DT, Pin.IN, Pin.PULL_UP),
    onRotateX,
)

def onRotateY(clockwise):
    global posY

    if clockwise == True:
        if posY < HEIGHT - 1:
            posY += 1
        else:
            posY = 0

    else:
        if posY == 0:
            posY = HEIGHT - 1
        else:
            posY -= 1

    addToHistory((posX, posY))
    updatePosAndShow()

rotaryY = RotaryEncoder(
    Pin(PIN_ROTARY_Y_CLK, Pin.IN, Pin.PULL_UP),
    Pin(PIN_ROTARY_Y_DT, Pin.IN, Pin.PULL_UP),
    onRotateY,
)

#######################################################################
# Main program

t = 500

updatePosAndShow()

while True:
    rotaryX.listenToRotation()
    rotaryY.listenToRotation()


    # onRotateX(random.choice([True, False]))
    # time.sleep_ms(20)
    # onRotateY(random.choice([True, False]))
    # time.sleep_ms(20)

    # onRotateX(random.choice([True, False]))
    # time.sleep_ms(t)
    # onRotateY(True)
    # time.sleep_ms(t)
    # onRotateY(True)
    # time.sleep_ms(t)