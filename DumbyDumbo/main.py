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

LEFT = 'LEFT'
RIGHT = 'RIGHT'
UP = 'UP'
DOWN = 'DOWN'

#######################################################################
# Global variables

cursorPosX = 0
cursorPosY = 0
cursorPrevPosX = cursorPosX
cursorPrevPosY = cursorPosY

cursorBlinkingOn = True
cursorBlinkTimestamp = 0

#######################################################################
# Init cursor

def moveCursor(direction):
    global cursorPosX
    global cursorPosY
    global cursorPrevPosX
    global cursorPrevPosY
    
    if direction == LEFT:
        if cursorPosX == 0:
            cursorPosX = WIDTH - 1
        else:
            cursorPosX -= 1
    elif direction == RIGHT:
        if cursorPosX < WIDTH - 1:
            cursorPosX += 1
        else:
            cursorPosX = 0
    elif direction == UP:
        if cursorPosY == 0:
            cursorPosY = HEIGHT - 1
        else:
            cursorPosY -= 1
    elif direction == DOWN:
        if cursorPosY < HEIGHT - 1:
            cursorPosY += 1
        else:
            cursorPosY = 0

    updateCursorPixel(cursorPrevPosX, cursorPrevPosY, False)

    cursorPrevPosX = cursorPosX
    cursorPrevPosY = cursorPosY

    updateCursorPixel(cursorPosX, cursorPosY, True)

    show()

def clickCursor():
    print('clickCursor', cursorPosX, cursorPosY)

    if findHistoryItem(cursorPosX, cursorPosY):
        history.remove((cursorPosX, cursorPosY))
        updatePixel(cursorPosX, cursorPosY, CURSOR_COLOR_ON)
    else:
        history.append((cursorPosX, cursorPosY))
        updatePixel(cursorPosX, cursorPosY, COLOR_ON)
    
    show()

def updateCursorPixel(x, y, isOn):
    if isOn:
        updatePixel(x,y,CURSOR_COLOR_ON)
    else:
        if findHistoryItem(x, y):
            updatePixel(x,y,COLOR_ON)
        else:
            updatePixel(x,y,CURSOR_COLOR_OFF)

def findHistoryItem(x,y):
    for item in history:
        if item == (x, y):
            return item
    return None

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
    if clockwise == True:
        moveCursor('RIGHT')
    else:
        moveCursor('LEFT')

rotaryX = RotaryEncoder(
    Pin(PIN_ROTARY_X_CLK, Pin.IN, Pin.PULL_UP),
    Pin(PIN_ROTARY_X_DT, Pin.IN, Pin.PULL_UP),
    Pin(PIN_ROTARY_X_SW, Pin.IN, Pin.PULL_UP),
    onRotateX,
    clickCursor
)

def onRotateY(clockwise):
    global posY

    if clockwise == True:
        moveCursor('DOWN')
    else:
        moveCursor('UP')

rotaryY = RotaryEncoder(
    Pin(PIN_ROTARY_Y_CLK, Pin.IN, Pin.PULL_UP),
    Pin(PIN_ROTARY_Y_DT, Pin.IN, Pin.PULL_UP),
    Pin(PIN_ROTARY_Y_SW, Pin.IN, Pin.PULL_UP),
    onRotateY,
    clickCursor
)

#######################################################################
# Main program

updatePosAndShow()

while True:
    rotaryX.listenToRotation()
    rotaryY.listenToRotation()

    # updateCursorBlink()