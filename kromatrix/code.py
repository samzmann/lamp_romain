from adafruit_led_animation.helper import PixelMap
from neopio import NeoPIO
import board
import random
import supervisor
from rotary_encoder import RotaryEncoder

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
    for item in history:
        if item == (x, y):
            return item
    return None

history = []

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

def updatePixel(x, y, colorRgb):
    strips[x][y] = colorRgb

def show():
    rawPixelsA.show()
    rawPixelsB.show()

#######################################################################
# Rotary encoder init

def onRotateX(clockwise):
    print('onRotateX', clockwise)
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
    print('onRotateY', clockwise)

    if clockwise == True:
        moveCursor('DOWN')
    else:
        moveCursor('UP')

rotaryY = RotaryEncoder(
    board.GP3,
    board.GP4,
    board.GP4,
    onRotateY,
    clickCursor
)

######################################################################
# Main program

# updatePosAndShow()

while True:
    rotaryX.listenToRotation()
    rotaryY.listenToRotation()

    updateCursorBlink()
