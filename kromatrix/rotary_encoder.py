import rotaryio

class RotaryEncoder():
    def __init__(self, clkPin, dtPin, swPin, onRotate, onCLick) -> None:

        self.encoder = rotaryio.IncrementalEncoder(clkPin, dtPin, divisor=2)
        # self.SW_PIN = digitalio.DigitalInOut(swPin)
        
        self.prevRotaryVal = 0

        # self.prevButtonVal = self.SW_PIN.value
        
        self.onCLick = onCLick
        self.onRotate = onRotate

    def listenToRotation(self):
        if self.encoder.position is not self.prevRotaryVal:
            print(self.encoder.position)
            isRotatingClockwise = self.encoder.position > self.prevRotaryVal
            print('isRotatingClockwise',isRotatingClockwise)
            self.prevRotaryVal = self.encoder.position