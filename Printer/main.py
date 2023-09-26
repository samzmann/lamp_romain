import machine
import board
import digitalio
import time
import busio
import adafruit_thermal_printer

uart = busio.UART(board.GP0, board.GP1, baudrate=9600)

ThermalPrinter = adafruit_thermal_printer.get_printer_class(1.11)
printer = ThermalPrinter(uart)

#printer.bold = True

l1 = '100000000010000000001000000000'
l2 = '.###.'
l3 = '..#..'

def pCorss():
    printer.feed(2)
    printer.print(l1)
    printer.print(l2)
    printer.print(l3)
    printer.feed(2)

    print('done')
    
def p(x):
    printer.print(x)
    printer.feed(2)
