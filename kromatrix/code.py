from adafruit_led_animation.helper import PixelMap
from adafruit_led_animation.group import AnimationGroup

from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase

from adafruit_led_animation.color import PURPLE, AMBER, JADE

import adafruit_fancyled.adafruit_fancyled as fancy

from neopio import NeoPIO
import board
import random
import supervisor
from rotary_encoder import RotaryEncoder
from switch import Switch
import time
import math

#######################################################################
# Constants

WIDTH = 13 # production
HEIGHT = 18 # production
# WIDTH = 8
# HEIGHT = 10

num_strands_a = 8 # production
num_strands_b = 5 # production
# num_strands_a = 8
# num_strands_b = 0

strand_length = HEIGHT

LEFT = 'LEFT'
RIGHT = 'RIGHT'
UP = 'UP'
DOWN = 'DOWN'

MODE_DRAW = 'MODE_DRAW'
MODE_COLOR_SNAKE = 'MODE_COLOR_SNAKE'

CURSOR_BLINK_DURATION_MS = 500

CURSOR_COLOR_ON = (0,255,0)
COLOR_ON = (255,0,0)
COLOR_OFF = (0,0,0)

RESET_DURATION_MS = 1000

#######################################################################
# Global variables

mode = MODE_DRAW

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

def resetCursor():
    global cursorPosX
    global cursorPosY
    global cursorPrevPosX
    global cursorPrevPosY
    global cursorBlinkingOn

    # cursorPosX = 0
    # cursorPosY = 0
    cursorPosX = math.floor(WIDTH / 2)
    cursorPosY = math.floor(HEIGHT / 2)
    cursorPrevPosX = cursorPosX
    cursorPrevPosY = cursorPosY

    cursorBlinkingOn = True

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

    
    if mode == MODE_DRAW:
        updateCursorDrawMode()
    if mode == MODE_COLOR_SNAKE:
        updateCursorColorSnakeMode()

def updateCursorDrawMode():
    global cursorPrevPosX
    global cursorPrevPosY

    updateCursorPixel(cursorPrevPosX, cursorPrevPosY, False)

    cursorPrevPosX = cursorPosX
    cursorPrevPosY = cursorPosY

    updateCursorPixel(cursorPosX, cursorPosY, True)

    show()

SNAKE_HISTORY_MAX_LENGTH = 30
snakeHistory = []

hueOffset = 0
hueOffsetTimestamp = 0
HUE_OFFSET_INCREMENT = 5
HUE_OFFSET_INCREMENT_INTERVAL_MS = 100

def updateHueOffset():
    global hueOffset
    global hueOffsetTimestamp

    now = supervisor.ticks_ms()

    detectTicksOverflow(now, hueOffsetTimestamp)

    if now > hueOffsetTimestamp + HUE_OFFSET_INCREMENT_INTERVAL_MS:
        hueOffset += HUE_OFFSET_INCREMENT
        hueOffsetTimestamp = now
        showColorSnake()

def showColorSnake():
    if len(snakeHistory) > SNAKE_HISTORY_MAX_LENGTH:
        x,y = snakeHistory[0]
        updatePixel(x, y, COLOR_OFF)
        snakeHistory.pop(0)

    for index in range(len(snakeHistory)):
        x, y = snakeHistory[index]

        MIN_HUE = 20
        MAX_HUE = 180
        
        hue = ((index * (MAX_HUE - MIN_HUE) / SNAKE_HISTORY_MAX_LENGTH + MIN_HUE) + hueOffset) / 255
        brightness = index * MAX_HUE / len(snakeHistory) / 255
        color = fancy.CHSV(hue, 255, brightness)
        
        updatePixel(x, y, color.pack())

    show()


def updateCursorColorSnakeMode():
    print('updateCusorColorSnakeMode')
    snakeHistory.append((cursorPosX, cursorPosY))

    showColorSnake()


def clickCursor():
    print('clickCursor', cursorPosX, cursorPosY)

    if findHistoryItem(cursorPosX, cursorPosY):
        history[cursorPosX][cursorPosY] = COLOR_OFF
        updatePixel(cursorPosX, cursorPosY, CURSOR_COLOR_ON)
    else:
        history[cursorPosX][cursorPosY] = COLOR_ON
        updatePixel(cursorPosX, cursorPosY, COLOR_ON)
    
    show()

def detectTicksOverflow(now, prevTimestamp):
    if now < prevTimestamp:
        print('timer overflow', now)
        supervisor.reload()

def updateCursorBlink():
    global cursorBlinkingOn
    global cursorBlinkTimestamp

    now = supervisor.ticks_ms()

    detectTicksOverflow(now, cursorBlinkTimestamp)

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
    board.GP10,
    board.GP11,
    board.GP12,
    num_strands_a * strand_length,
    num_strands=num_strands_a,
    auto_write=False,
    brightness=0.18,
)

rawPixelsB = NeoPIO(
    board.GP13,
    board.GP14,
    board.GP15,
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
    length = random.randrange(math.floor(HEIGHT * 0.1), math.floor(HEIGHT * 0.6))
    return Comet(strip, speed=RESET_DURATION_MS / 1000 / HEIGHT, color=JADE, tail_length=length, bounce=False)

animations = [make_animation(strip) for strip in strips]
chase = AnimationGroup(*animations, )

def generalReset():
    global resetTimestamp
    global isResetting
    resetTimestamp = supervisor.ticks_ms()
    isResetting = True


def resetDrawMode():
    print('resetDrawMode')
    global history

    generalReset()

    resetCursor()

    history = deep_copy(historyForReset)

def resetColorSnakeMode():
    global snakeHistory

    generalReset()

    resetCursor()

    snakeHistory = [(cursorPosX, cursorPosY)]


def completeReset():
    global isResetting
    global animations
    global chase

    print('completeReset')

    animations = [make_animation(strip) for strip in strips]
    chase = AnimationGroup(*animations, )

    isResetting = False

    for i in range(len(strips)):
        strips[i].fill(COLOR_OFF)
    show()

    if mode == MODE_COLOR_SNAKE:
        updateCursorColorSnakeMode()

    print('completeReset done')

#######################################################################
# Init Printer


def printGrid():
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

def onClickRotary():
    if mode == MODE_DRAW:
        clickCursor()

def onRotateX(clockwise):
    print('onRotateX')
    direction = RIGHT if clockwise else LEFT
    moveCursor(direction)

rotaryX = RotaryEncoder(
    board.GP16,
    board.GP17,
    board.GP18,
    onRotateX,
    onClickRotary
)

def onRotateY(clockwise):
    print('onRotateY')
    direction = DOWN if clockwise else UP
    moveCursor(direction)

rotaryY = RotaryEncoder(
    board.GP19,
    board.GP20,
    board.GP21,
    onRotateY,
    onClickRotary
)

def updateRotaries():
    rotaryX.listenToRotation()
    rotaryY.listenToRotation()

#######################################################################
# Switch init

def changeMode():
    global mode

    print('changeMode')
    if mode == MODE_DRAW:
        mode = MODE_COLOR_SNAKE
        onClickReset()
    else:
        mode = MODE_DRAW
        onClickReset()
    print('new mode:', mode)

def onClickReset():
    if mode == MODE_DRAW:
        resetDrawMode()
    if mode == MODE_COLOR_SNAKE:
        resetColorSnakeMode()

def onClickPrint():
    if mode == MODE_DRAW:
        printGrid()

modeSwitch = Switch(board.GP7, changeMode)
resetSwitch = Switch(board.GP8, onClickReset)
printSwitch = Switch(board.GP9, onClickPrint)

def updateSwitches():
    modeSwitch.update()
    resetSwitch.update()
    printSwitch.update()

######################################################################
# Main program

onClickReset()

def checkResetComplete():
    now = supervisor.ticks_ms()
    detectTicksOverflow(now, resetTimestamp)
    if now > resetTimestamp + RESET_DURATION_MS:
        completeReset()

def updateInputs():
    updateRotaries()
    updateSwitches()

while True:
    if isResetting == True:
        chase.animate()
        checkResetComplete()
    else:
        if mode == MODE_DRAW:
            updateInputs()
            updateCursorBlink()
        if mode == MODE_COLOR_SNAKE:
            updateInputs()
            updateHueOffset()