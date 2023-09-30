import board
import digitalio
from adafruit_debouncer import Debouncer

class Switch():
    def __init__(self, pin, onCLick) -> None:
        pin_input = digitalio.DigitalInOut (pin)
        pin_input.switch_to_input(pull=digitalio.Pull.UP)
        self.switch = Debouncer(pin_input)
        self.onCLick = onCLick

    def update(self):
            self.switch.update()
            if self.switch.fell:
                print("Just pressed")
                self.onCLick()