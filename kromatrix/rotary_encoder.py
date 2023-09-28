import digitalio
import rotaryio

class RotaryEncoder():
    def __init__(self, clkPin, dtPin, swPin, onRotate, onCLick) -> None:

        self.encoder = rotaryio.IncrementalEncoder(clkPin, dtPin, divisor=2)
        self.button = digitalio.DigitalInOut(swPin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP
        
        self.prevRotaryVal = 0
        self.prevButtonVal = None
        
        self.onCLick = onCLick
        self.onRotate = onRotate

    def listenToRotation(self):
        if self.encoder.position is not self.prevRotaryVal:
            print(self.encoder.position)
            isRotatingClockwise = self.encoder.position > self.prevRotaryVal
            self.onRotate(isRotatingClockwise)
            
            print('isRotatingClockwise',isRotatingClockwise)
            self.prevRotaryVal = self.encoder.position
        
        if not self.button and self.prevButtonVal is 0:
            self.prevButtonVal = 1
        if self.button and self.prevButtonVal == 1:
            print("Button pressed.")
            self.onCLick()

        if not self.button.value and self.prevButtonVal is None:
            self.prevButtonVal = "pressed"
        if self.button.value and self.prevButtonVal == "pressed":
            self.onCLick()
            self.prevButtonVal = None
