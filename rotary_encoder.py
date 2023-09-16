class RotaryEncoder():

    def __init__(self, clkPin, dtPin, onClockwise, onAntiClockwise) -> None:

        self.CLK_PIN = clkPin
        self.prevRotaryVal = clkPin.value()

        self.DT_PIN = dtPin

        self.onClockwise = onClockwise
        self.onAntiClockwise = onAntiClockwise


    def rotaryChanged(self):
        val = self.CLK_PIN.value()
        
        
        if val !=self. prevRotaryVal:
        
            
            if self.DT_PIN.value() == val:
                print("anti-clockwise")
                self.onAntiClockwise()
                    
                
            else:
                print("clockwise")
                self.onClockwise()
                
            self.prevRotaryVal = val