#Jessica Clara Fealy - 2021
#Macropad custom code

import time
import board
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

#This function will tell the computer the button is being help
#A key stroke every 0.1 seconds will be made
def MediaControlButtons(keysToPress, switch, state, switches):
    if(state == 0):
        cc.send(keysToPress)
    else:
        keyPressed = True
        while (keyPressed):
            if switches[switch].value:
                    try:
                        kbd.release(keysToPress)
                        keyPressed = False
                    except ValueError:
                        pass
                        switch_state[switch] = 0
            else:
                cc.send(keysToPress)
                time.sleep(0.1)
                
def PressKey(keysToPress, switch, state, switches):
    if(state == 0):
        kbd.send(keysToPress)
    else:
        keyPressed = True
        while (keyPressed):
            if switches[switch].value:
                    try:
                        kbd.release(keysToPress)
                        keyPressed = False
                    except ValueError:
                        pass
                        switch_state[switch] = 0
            else:
                kbd.send(keysToPress)
                time.sleep(0.1)
    


