import utime

class RotaryEncoder():

    def __init__(self, clkPin, dtPin, swPin, onRotate, onCLick) -> None:

        self.CLK_PIN = clkPin
        self.prevRotaryVal = clkPin.value()

        self.DT_PIN = dtPin

        self.SW_PIN = swPin
        self.prevButtonVal = swPin.value()
        self.onCLick = onCLick

        self.onRotate = onRotate


    def listenToRotation(self):
        val = self.CLK_PIN.value()
        
        
        if val !=self. prevRotaryVal:

            isRotatingClockwise = self.DT_PIN.value() != val
            self.onRotate(isRotatingClockwise)

            self.prevRotaryVal = val

        if self.SW_PIN.value() == 0 and self.SW_PIN.value() != self.prevButtonVal:
            self.onCLick()
            utime.sleep_ms(200)