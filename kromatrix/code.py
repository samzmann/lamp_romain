from adafruit_led_animation.helper import PixelMap
from adafruit_led_animation.group import AnimationGroup

from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase

from adafruit_led_animation.color import PURPLE, AMBER, JADE



from neopio import NeoPIO
import board
import random
import supervisor
from rotary_encoder import RotaryEncoder
import time
import supervisor
import math

#######################################################################
# Constants

WIDTH = 8
HEIGHT = 10

# Customize for your strands here
num_strands_a = 6
num_strands_b = 2

strand_length = HEIGHT

LEFT = 'LEFT'
RIGHT = 'RIGHT'
UP = 'UP'
DOWN = 'DOWN'

CURSOR_BLINK_DURATION_MS = 500

CURSOR_COLOR_ON = (0,255,0)
COLOR_ON = (255,0,0)
COLOR_OFF = (0,0,0)

RESET_DURATION_MS = 1000

#######################################################################
# Global variables

cursorPosX = 0
cursorPosY = 0
cursorPrevPosX = cursorPosX
cursorPrevPosY = cursorPosY

cursorBlinkingOn = True
cursorBlinkTimestamp = 0


isResetting = False
resetTimestamp = 0

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
        history[cursorPosX][cursorPosY] = COLOR_OFF
        updatePixel(cursorPosX, cursorPosY, CURSOR_COLOR_ON)
    else:
        history[cursorPosX][cursorPosY] = COLOR_ON
        updatePixel(cursorPosX, cursorPosY, COLOR_ON)
    
    show()

def updateCursorBlink():
    global cursorBlinkingOn
    global cursorBlinkTimestamp

    now = supervisor.ticks_ms()

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
            updatePixel(x,y,COLOR_OFF)

def findHistoryItem(x,y):
    item = history[x][y]
    if item == (0,0,0):
        return None
    return item

#######################################################################
# Init Neopixels

rawPixelsA = NeoPIO(
    board.GP13,
    board.GP14,
    board.GP15,
    num_strands_a * strand_length,
    num_strands=num_strands_a,
    auto_write=False,
    brightness=0.18,
)

rawPixelsB = NeoPIO(
    board.GP10,
    board.GP11,
    board.GP12,
    num_strands_b * strand_length,
    num_strands=num_strands_b,
    auto_write=False,
    brightness=0.18,
)

strips = [
    PixelMap(
        rawPixelsA,
        range(i * strand_length, (i + 1) * strand_length),
        individual_pixels=True,
    )
    for i in range(num_strands_a)
] + [
    PixelMap(
        rawPixelsB,
        range(i * strand_length, (i + 1) * strand_length),
        individual_pixels=True,
    )
    for i in range(num_strands_b)
]

def deep_copy(lst):
    return [list(sublist) for sublist in lst]

historyForReset = deep_copy(strips)
history = deep_copy(strips)

def updatePixel(x, y, colorRgb):
    strips[x][y] = colorRgb

def show():
    rawPixelsA.show()
    rawPixelsB.show()

def make_animation(strip):
    length = random.randrange(math.floor(HEIGHT * 0.2), math.floor(HEIGHT * 0.6))
    return Comet(strip, speed=RESET_DURATION_MS / 1000 / HEIGHT, color=JADE, tail_length=length, bounce=False)

animations = [make_animation(strip) for strip in strips]
chase = AnimationGroup(*animations, )

def reset():

    global resetTimestamp
    resetTimestamp = supervisor.ticks_ms()

    global cursorPosX
    global cursorPosY
    global cursorPrevPosX
    global cursorPrevPosY
    global cursorBlinkingOn
    global strips
    global history

    global isResetting

    cursorPosX = 0
    cursorPosY = 0
    cursorPrevPosX = cursorPosX
    cursorPrevPosY = cursorPosY

    cursorBlinkingOn = True

    history = deep_copy(historyForReset)

    isResetting = True

def completeReset():
    global isResetting
    global animations
    global chase


    for strip in strips:
        strip.fill(COLOR_OFF)
    show()

    animations = [make_animation(strip) for strip in strips]
    chase = AnimationGroup(*animations, )

    isResetting = False

#######################################################################
# Init Printer


def printGrid():
    print('printGrid')
    lines = []
    # Loop through each row of the grid
    for row in range(len(history[0])):
        # Create a new list to store the items in the current row
        current_row = []
        
        # Loop through each column of the grid
        for col in range(len(history)):
            if history[col][row] == COLOR_OFF:
                current_row.append('_')
            else:
                current_row.append('X')
        
        # Join the items in the current row into a single string and append it to the result list
        lines.append(''.join(current_row))
    
    for line in lines:
        print(line)

#######################################################################
# Rotary encoder init

def onRotateX(clockwise):
    if clockwise == True:
        moveCursor('RIGHT')
    else:
        moveCursor('LEFT')

rotaryX = RotaryEncoder(
    board.GP0,
    board.GP1,
    board.GP2,
    onRotateX,
    clickCursor
)

def onRotateY(clockwise):
    if clockwise == True:
        moveCursor('DOWN')
    else:
        moveCursor('UP')

rotaryY = RotaryEncoder(
    board.GP3,
    board.GP4,
    board.GP5,
    onRotateY,
    reset
)

######################################################################
# Main program

# updatePosAndShow()

def checkResetComplete():
    now = supervisor.ticks_ms()
    if now > resetTimestamp + RESET_DURATION_MS:
        completeReset()

while True:
    if isResetting == True:
        chase.animate()
        checkResetComplete()
    else:
        rotaryX.listenToRotation()
        rotaryY.listenToRotation()
        
        updateCursorBlink()
