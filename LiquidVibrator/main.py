from tm1637 import TM1637
from machine import Pin, ADC, PWM
import time

#######################################################################
# Pins

DISPLAY_DIO_PIN = 17
DISPLAY_CLK_PIN = 16

SLIDER_PIN = 26

LED_BUITLTIN = 25

MOTOR_ENA = 0
MOTOR_IN1 = 1
MOTOR_IN2 = 2

#######################################################################
# Constants

MOTOR_MIN = 0
MOTOR_MAX = 100

SLIDER_MIN = 400
SLIDER_MAX = 65400

#######################################################################
# Utils

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max - in_min) + out_min)

#######################################################################
# Display init

display = TM1637(clk=Pin(DISPLAY_CLK_PIN), dio=Pin(DISPLAY_DIO_PIN))

#######################################################################
# Slider potentiometer init

slider = ADC(SLIDER_PIN)

pwm_led = PWM(Pin(LED_BUITLTIN, mode=Pin.OUT)) 
pwm_led.freq(1_000)


#######################################################################
# Motor init
In1 = Pin(MOTOR_IN1, Pin.OUT)
In2 = Pin(MOTOR_IN2, Pin.OUT)

In1.high()
In2.low()

EN_A = PWM(Pin(MOTOR_ENA, Pin.OUT))
EN_A.freq(1000)

#######################################################################
# Main program


while True:
    sliderVal = slider.read_u16()
    pwm_led.duty_u16(-sliderVal)
    # time.sleep(1)
    
    EN_A.duty_u16(-sliderVal)

    mapped = map(sliderVal, SLIDER_MIN, SLIDER_MAX, MOTOR_MAX, MOTOR_MIN)
    display.number(mapped)

