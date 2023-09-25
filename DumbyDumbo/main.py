import math
from machine import Pin
from neopixel import Neopixel
from rotary_encoder import RotaryEncoder
import time
import utime
import random
from cursor import Cursor

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
PIN_ROTARY_X_SW = 9

PIN_ROTARY_Y_CLK = 7
PIN_ROTARY_Y_DT = 8
PIN_ROTARY_Y_SW = 10

#######################################################################
# Constants

WIDTH = 5
HEIGHT = 10

COLOR_ON = (0,255,50)
COLOR_OFF = (0,0,0)

MIN_HUE = 30000
MAX_HUE = 65535

HISTORY_MIN_LENGTH = 1
HISTORY_MAX_LENGTH = 10

CURSOR_BLINK_DURATION_MS = 500
CURSOR_COLOR_ON = (10000, 255, 50)
CURSOR_COLOR_OFF = (0, 0, 0)

#######################################################################
# Global variables

cursorPosX = 0
cursorPosY = 0
cursorBlinkingOn = True
cursorBlinkTimestamp = 0

posX = 0

posY = 0

history = []

#######################################################################
# Neopixel init

strips = [
    Neopixel(HEIGHT, 0, PIN_STRIP_0, "GRB"),
    Neopixel(HEIGHT, 1, PIN_STRIP_1, "GRB"),
    Neopixel(HEIGHT, 2, PIN_STRIP_2, "GRB"),
    Neopixel(HEIGHT, 3, PIN_STRIP_3, "GRB"),
    Neopixel(HEIGHT, 4, PIN_STRIP_4, "GRB"),
]

def updatePixel(x, y, colorHsv):
    h,s,v = colorHsv
    strips[x].set_pixel(y, strips[x].colorHSV(h,s,v))

def show():
    for stripIndex in range(WIDTH):
        strips[stripIndex].show()

def addToHistory(coordinates):
    history.append(coordinates)

def showCursor():

    if cursorBlinkingOn:
        updatePixel(cursorPosX, cursorPosY, CURSOR_COLOR_ON)
    elif ([item for item in history if (item[0] == cursorPosX and item[1] == cursorPosY)]):
        updatePixel(cursorPosX, cursorPosY, COLOR_ON)
    else:
        updatePixel(cursorPosX, cursorPosY, CURSOR_COLOR_OFF)

    show()

def updateCursorPos(x, y):
    print('updateCursorPos')

    global cursorPosX
    global cursorPosY
    global cursorBlinkingOn
    global cursorBlinkTimestamp

    itemOnPos = [item for item in history if (item[0] == x and item[1] == y)]
    print('itemOnPos', itemOnPos)

    if ([item for item in history if (item[0] == x and item[1] == y)]):
         print('item found')
         updatePixel(x, y, COLOR_ON)
    else:
        print('item not found')
        # Turn off previous cursor pixel
        updatePixel(cursorPosX, cursorPosY, CURSOR_COLOR_OFF)

    # Force blink on
    cursorBlinkingOn = True
    cursorBlinkTimestamp = utime.ticks_ms()

    cursorPosX = x
    cursorPosY = y
    showCursor()

def updateCursorBlink():
    global cursorBlinkingOn
    global cursorBlinkTimestamp

    now = utime.ticks_ms()

    if now > cursorBlinkTimestamp + CURSOR_BLINK_DURATION_MS:
        cursorBlinkingOn = not cursorBlinkingOn
        cursorBlinkTimestamp = now
        showCursor()
        
def updatePosAndShow():
    print('updatePosAndShow')
    for index in range(len(history)):
        x, y = history[index]
        updatePixel(x, y, COLOR_ON)


    show()

#######################################################################
# Cursor init

def updateAndShowCursor(posX, posY, colorHsv):
    updatePixel(posX,posY,colorHsv)
    show()

cursor = Cursor(updateAndShowCursor)

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

    updateCursorPos(posX, cursorPosY)
    updatePosAndShow()

def onClickX():
    print('onClickX')
    addToHistory((cursorPosX, cursorPosY))
    updatePosAndShow()

rotaryX = RotaryEncoder(
    Pin(PIN_ROTARY_X_CLK, Pin.IN, Pin.PULL_UP),
    Pin(PIN_ROTARY_X_DT, Pin.IN, Pin.PULL_UP),
    Pin(PIN_ROTARY_X_SW, Pin.IN, Pin.PULL_UP),
    onRotateX,
    onClickX
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

    updateCursorPos(cursorPosX, posY)
    updatePosAndShow()

def onClickY():
    print('onClickY')
    addToHistory((cursorPosX, cursorPosY))
    updatePosAndShow()

rotaryY = RotaryEncoder(
    Pin(PIN_ROTARY_Y_CLK, Pin.IN, Pin.PULL_UP),
    Pin(PIN_ROTARY_Y_DT, Pin.IN, Pin.PULL_UP),
    Pin(PIN_ROTARY_Y_SW, Pin.IN, Pin.PULL_UP),
    onRotateY,
    onClickY
)

#######################################################################
# Main program

t = 500

updatePosAndShow()

while True:
    rotaryX.listenToRotation()
    rotaryY.listenToRotation()

    updateCursorBlink()


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