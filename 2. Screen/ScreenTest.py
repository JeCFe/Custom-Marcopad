import os
import time
import busio
import board
import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label


displayio.release_displays()
SDA = board.GP0
SCL = board.GP1
i2c = busio.I2C(SCL, SDA)


display_bus = displayio.I2CDisplay (i2c, device_address = 0x3C)
color_bitmap = displayio.Bitmap(128, 64, 1)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)
splash = displayio.Group(scale=2, x=0, y=0)
display.show(splash)
text_area = label.Label(terminalio.FONT, text=""*20, color=0xFFFF00, x=1, y=5)
splash.append(text_area)


def GetText():
    return text_area.text

def UpdateScreen(message):
    text_area.text=message

        
