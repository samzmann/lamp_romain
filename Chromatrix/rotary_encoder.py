class RotaryEncoder():

    def __init__(self, clkPin, dtPin, onRotate) -> None:

        self.CLK_PIN = clkPin
        self.prevRotaryVal = clkPin.value()

        self.DT_PIN = dtPin

        self.onRotate = onRotate


    def listenToRotation(self):
        val = self.CLK_PIN.value()
        
        
        if val !=self. prevRotaryVal:

            isRotatingClockwise = self.DT_PIN.value() != val
            self.onRotate(isRotatingClockwise)

            self.prevRotaryVal = val