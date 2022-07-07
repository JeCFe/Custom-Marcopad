# Jessica Clara Fealy - 2021
# Macropad custom code

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
import MacropadClass as MC
#from ScreenTest import UpdateScreen as US
#from ScreenTest import GetText as GT

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


    # TOP ROW
    board.GP21,
    board.GP20,
    board.GP19,
        # MIDDLE ROW
    board.GP6,
    board.GP7,
    board.GP8,
        # BOTTOM ROW
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
# Initalises all keys
for i in range(9):
    switches[i] = DigitalInOut(pins[i])
    switches[i].direction = Direction.INPUT
    switches[i].pull = Pull.UP

switch_state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
print("---Initalisation Complete---")
print("---Welcome to the Macropad---")
#US("Welcome")


def SetTime():
    global currentTime
    global futureTime
    global StandbyMode

    currentTime = time.time()
    futureTime = currentTime + 10
    StandbyMode = False


# Call functions from their registeries
def FunctionManager(functionReg):

    global mode
    print("Current layer: "+str(mode))
    print(functionReg)
    buttonName = MC.macroPad[mode].GetButtonName(functionReg)
    buttonOperation = MC.macroPad[mode].GetButtonOperation(functionReg)
    print(buttonName)
    print(functionReg)
    
    if(buttonOperation == "ModeSwitch"):
        print("layer length: " + str(MC.GetMacroPadLayerLength()))
        mode = ((mode+1)%MC.GetMacroPadLayerLength())
        print("Current layer: " + str(mode))
        print(MC.macroPad[mode].GetLayerName())

    #time.sleep(2)
   # US("Mode:   " + str(mode))


MC.ReadFromFile()
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
        time.sleep(0.01)  # debounce
