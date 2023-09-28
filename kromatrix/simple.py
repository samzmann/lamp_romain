import rotaryio
import board

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

        # if self.SW_PIN.value == 0 and self.SW_PIN.value != self.prevButtonVal:
        #     self.onCLick()
        #     utime.sleep_ms(200)

def onRotateX(clockwise):
    print('onRotateX', clockwise)

def onRotateY(clockwise):
    print('onRotateY', clockwise)

def clickCursor():
    print('clickCursor')

rotaryX = RotaryEncoder(
    board.GP0,
    board.GP1,
    board.GP2,
    onRotateX,
    clickCursor
)

rotaryY = RotaryEncoder(
    board.GP3,
    board.GP4,
    board.GP4,
    onRotateY,
    clickCursor
)

while True:
    rotaryX.listenToRotation()
    rotaryY.listenToRotation()