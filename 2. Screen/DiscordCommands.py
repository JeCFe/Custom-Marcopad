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

#Time delay to allow discord opening animation to complete before next command
sleepConstant = 0.15

#Some discord commands requires the overlay to be opened
def AccessDiscordOverlay():
    kbd.send(Keycode.F20)
    
#Sleeps program for the time constant variable
def TimeDelay():
    time.sleep(sleepConstant)
    
#Mutes discord and mutes mic
def Deafen():
    kbd.send(Keycode.F18)

#Only works in games recognised by discord
#Unique command needs to be set up in discord
def GameScreenShare():
    kbd.send(Keycode.F19)

#Mutes mic
def ToggleMute():
    kbd.send(Keycode.F15)

#Activates pust to talk
def PushToTalk(switch, switches):
    keyPressed = True;
    while(keyPressed):
        if(switches[switch].value): #If key is released
            try:
                kbd.release(Keycode.F16)
                keyPressed = False
            except ValueError:
                    pass
                    switch_state[switch] = 0
        else:#If key continue to be held
            kbd.press(Keycode.F16)
            
        
    
    
