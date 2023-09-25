import utime
    
class Cursor():
    posX = 0
    posY = 0
    isBlinkingOn = True
    blinkDuration = 200
    blinkTimestamp = 0

    colorOn = (10000, 255, 155)
    colorOff = (0, 0, 0)
        
    def __init__(self, updatePixelAndShow) -> None:
        self.updatePixelAndShow = updatePixelAndShow

    def setPosX(self,value):
        self.posX = value

    def setPosY(self,value):
        self.posY = value

    def update(self):
        now = utime.ticks_ms()

        if now > self.blinkTimestamp + self.blinkDuration:
            self.isBlinkingOn = not self.isBlinkingOn
            self.blinkTimestamp = now
            self.show()

    def show(self):
        color = self.colorOn if self.isBlinkingOn else self.colorOff
        self.updatePixelAndShow(self.posX, self.posY, color)
