# SPDX-FileCopyrightText: 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import random
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.helper import PixelMap
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.color import PURPLE, AMBER, JADE

from neopio import NeoPIO
import board

# Customize for your strands here
num_strands = 12
strand_length = 10

pixels0 = NeoPIO(
    board.GP10,
    board.GP11,
    board.GP12,
    4 * strand_length,
    num_strands=4,
    auto_write=False,
    brightness=0.18,
)

pixels1 = NeoPIO(
    board.GP13,
    board.GP14,
    board.GP15,
    8 * strand_length,
    num_strands=8,
    auto_write=False,
    brightness=0.18,
)

# Make a virtual PixelMap so that each strip can be controlled independently
strips0 = [
    PixelMap(
        pixels0,
        range(i * strand_length, (i + 1) * strand_length),
        individual_pixels=True,
    )
    for i in range(4)
]
strips1 = [
    PixelMap(
        pixels1,
        range(i * strand_length, (i + 1) * strand_length),
        individual_pixels=True,
    )
    for i in range(8)
]

strips = strips0 + strips1

# This function makes a comet animation with slightly random settings
def makeRainbowCometAnimation(strip):
    speed = (1 + random.random()) * 0.02
    length = random.randrange(18, 22)
    bounce = random.random() > 0.5
    offset = random.randint(0, 255)
    return RainbowComet(
        strip, speed=speed, tail_length=length, bounce=bounce, colorwheel_offset=offset
    )


def makeChaseAnimation(strip):
    return Chase(strip, speed=0.1, size=3, spacing=6, color=AMBER)


def makeSparkleAnimation(strip):
    speed = (1 + random.random()) * 0.05
    return Sparkle(strip, speed=speed, color=AMBER)


# Make an animation for each virtual strip
animations = [makeRainbowCometAnimation(strip) for strip in strips]
#animations = [makeChaseAnimation(strip) for strip in strips]
#animations = [makeSparkleAnimation(strip) for strip in strips]

# animations = [
#    makeRainbowCometAnimation(strips[0]),
#    chase
# ]

# Put the animations into a group so that we can animate them together
group = AnimationGroup(
    *animations,
)


def a():
    print("a")


# Show the animations forever
while True:
    group.animate()
