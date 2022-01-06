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
from ScreenTest import UpdateScreen as US
from ScreenTest import GetText as GT



print("---Initalisation Starting--- ")
FUNCTION = 3
KEY = 1
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True
mode = 0
kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

currentTime = 0
futureTime = 0
StandbyMode = False

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
US("Welcome")
       
def SetTime():
    global currentTime
    global futureTime
    global StandbyMode
    
    currentTime = time.time()
    futureTime = currentTime + 10
    StandbyMode = False
           
#Call functions from their registeries
def FunctionManager(functionReg):
    global mode
    #These options are persistant 
    if functionReg == 0:#Bottom Left#
        US("Vol Down")
        BCC.MediaControlButtons(ConsumerControlCode.VOLUME_DECREMENT, functionReg, 1, switches)
        
    if functionReg == 1:#Bottom Middle
        US("Mute")
        BCC.MediaControlButtons(ConsumerControlCode.MUTE, functionReg, 0, switches)

    if functionReg == 2: #Bottom Right
        US("Vol Up")
        BCC.MediaControlButtons(ConsumerControlCode.VOLUME_INCREMENT, functionReg, 1, switches)

    #These macros have options applied
    if functionReg == 3: #Middel Left
        if(mode == 0):#Mode 1
            US("Previous")
            BCC.MediaControlButtons(ConsumerControlCode.SCAN_PREVIOUS_TRACK, functionReg, 1, switches)
        else:#Mode 2
            US("Overlay")
            DCS.AccessDiscordOverlay()
        
    if functionReg == 4: #Middle Middle
        if(mode == 0):
            US("Play/Pause")
            BCC.MediaControlButtons(ConsumerControlCode.PLAY_PAUSE, functionReg, 0, switches)
        else:
            US("P to T")
            DCS.PushToTalk(functionReg, switches)
         
    if functionReg == 5: #Middle Right
        if(mode == 0):
            US("Next")
            BCC.MediaControlButtons(ConsumerControlCode.SCAN_NEXT_TRACK, functionReg, 1, switches)
        else:
            US("Dis Mute")
            DCS.ToggleMute()
        
    #Mode change 
    if functionReg == 6: #Top Left
        US("Mode")
        mode = (mode+1)%2
        
    if functionReg == 7:#Top Middle
        US("Copy")
        if(mode == 0):
            kbd.send(Keycode.CONTROL, Keycode.C)            
        else:
            US("Dis Deafen")
            DCS.Deafen()
            
    if functionReg == 8:#Top Right
        if(mode == 0):
            US("Paste")
            kbd.send(Keycode.CONTROL, Keycode.V)
        else:
            US("Game Share")
            DCS.GameScreenShare()
        
    time.sleep(2)
    US("Mode:   "+str(mode))

SetTime()
while True:
    for button in range(9):
        if switch_state[button] == 0:
            if not switches[button].value:
                try:
                    if keymap[button][0] == FUNCTION:
                        FunctionManager(keymap[button][1])
                        SetTime()
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
    if StandbyMode == False:    
        comparisionTime = time.time()
        if comparisionTime >= futureTime:
                CurrentText = GT()
                US("Standby")
                time.sleep(5)
                US("")
                StandbyMode = True

            
    time.sleep(0.01)  # debounce