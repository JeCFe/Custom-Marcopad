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
import ButtonControlCode as BCC
import DiscordCommands as DCS

print("---Initalisation Starting--- ")
FUNCTION = 3
KEY = 1
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True
mode = 0
kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
# list of pins to use (skipping GP15 on Pico because it's funky)
pins = [
    #MIDDLE ROW
    board.GP4,
    board.GP5,
    board.GP6, 
    #BOTTOM ROW
    board.GP7,
    board.GP8,
    board.GP9,     
    #TOP ROW
    board.GP10,
    board.GP11,
    board.GP12,
]
keymap = {
    (0): (FUNCTION, 0),
    (1): (FUNCTION, 1),
    (2): (FUNCTION, 2),
    (3): (FUNCTION, 3),
    (4): (FUNCTION, 4),
    (5): (FUNCTION, 5),
    (6): (FUNCTION, 6),
    (7): (FUNCTION, 7),
    (8): (FUNCTION, 8)
}
switches = [0, 1, 2, 3, 4, 5, 6,
            7, 8]
#Initalises all keys
for i in range(9):
    switches[i] = DigitalInOut(pins[i])
    switches[i].direction = Direction.INPUT
    switches[i].pull = Pull.UP

switch_state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
print("---Initalisation Complete---")
print("---Welcome to the Macropad---")

         
           
#Call functions from their registeries
def FunctionManager(functionReg):
    global mode
    #These options are persistant 
    if functionReg == 0:#Bottom Left
        BCC.MediaControlButtons(ConsumerControlCode.VOLUME_DECREMENT, functionReg, 1, switches)
    if functionReg == 1:#Bottom Middle
        BCC.MediaControlButtons(ConsumerControlCode.MUTE, functionReg, 0, switches)        
    if functionReg == 2: #Bottom Right
        BCC.MediaControlButtons(ConsumerControlCode.VOLUME_INCREMENT, functionReg, 1, switches)
        
    #These macros have options applied
    if functionReg == 3: #Middel Left
        if(mode == 0):#Mode 1
            BCC.MediaControlButtons(ConsumerControlCode.SCAN_PREVIOUS_TRACK, functionReg, 1, switches)
        else:#Mode 2
            DCS.AccessDiscordOverlay()
        
        
    if functionReg == 4: #Middle Middle
        if(mode == 0):
            BCC.MediaControlButtons(ConsumerControlCode.PLAY_PAUSE, functionReg, 0, switches)
        else:
            DCS.PushToTalk(functionReg, switches)
         
    if functionReg == 5: #Middle Right
        if(mode == 0):
            BCC.MediaControlButtons(ConsumerControlCode.SCAN_NEXT_TRACK, functionReg, 1, switches)
        else:
            DCS.ToggleMute()
            
        
        
    #Mode change 
    if functionReg == 6: #Top Left
        mode = (mode+1)%2
        print(mode)
        print(functionReg)
        
    if functionReg == 7:#Top Middle
        if(mode == 0):
            kbd.send(Keycode.CONTROL, Keycode.C)            
        else:
            DCS.Deafen()
            
    if functionReg == 8:#Top Right
        if(mode == 0):
            kbd.send(Keycode.CONTROL, Keycode.V)
        else:
            DCS.GameScreenShare()
        

        
while True:
    for button in range(9):
        if switch_state[button] == 0:
            if not switches[button].value:
                try:
                    if keymap[button][0] == FUNCTION:
                        FunctionManager(keymap[button][1])
                except ValueError:  # deals w six key limit
                    pass
                switch_state[button] = 1

        if switch_state[button] == 1:
            if switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.release(*keymap[button][1])

                except ValueError:
                    pass
                switch_state[button] = 0

    time.sleep(0.01)  # debounce