import math
from machine import Pin
from neopixel import Neopixel
from rotary_encoder import RotaryEncoder
import time
import utime
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
PIN_ROTARY_X_SW = 9

PIN_ROTARY_Y_CLK = 7
PIN_ROTARY_Y_DT = 8
PIN_ROTARY_Y_SW = 10

#######################################################################
# Constants

WIDTH = 5
HEIGHT = 10

MIN_HUE = 30000
MAX_HUE = 65535

COLOR_ON = (0,255,50)
COLOR_OFF = (0,0,0)

COLOR_GREEN = (20000,255,50)

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

def updateCursorBlink():
    global cursorBlinkingOn
    global cursorBlinkTimestamp

    now = utime.ticks_ms()

    if now > cursorBlinkTimestamp + CURSOR_BLINK_DURATION_MS:
        cursorBlinkingOn = not cursorBlinkingOn
        cursorBlinkTimestamp = now
        updateCursorPixel(cursorPosX, cursorPosY, cursorBlinkingOn)
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
        
def updatePosAndShow():
    print('updatePosAndShow')
    for index in range(len(history)):
        x, y = history[index]
        updatePixel(x, y, COLOR_ON)

    show()

#######################################################################
# Animations

def runResetAnim():

    historyLength = 3
    rowHistory = []

    def doAnim():
        row = 0

        while row <= HEIGHT:
            for i in range(WIDTH):

                print('1. ', i, row)

                if row != HEIGHT:
                    updatePixel(i, row, COLOR_GREEN)
                
                if row > 0:
                    for r in reversed(range(row, max(row - historyLength, 0))):
                        print('range HEIGHT', r)
                        if r < row:
                            distance = row - r
                            if distance < historyLength and rowHistory[row - distance][i]:
                                brightnessRatio = math.floor((distance / historyLength) * 200)
                                updatePixel(i, distance, (20000, 255, brightnessRatio))
                            else:
                                print('2.', i, distance)
                                updatePixel(i, distance, COLOR_OFF)

            show()
            time.sleep_ms(100)
            
            print('---')
                
            row +=1

    for i in range(HEIGHT):
        rowHistory.append([])
        for j in range(WIDTH):
            rowHistory[i].append(random.choice([True, False, False]))

        if i == HEIGHT - 1:
            print('rowHistory', rowHistory)

            doAnim()

runResetAnim() 

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

# updatePosAndShow()

# while True:
#     rotaryX.listenToRotation()
#     rotaryY.listenToRotation()

#     updateCursorBlink()