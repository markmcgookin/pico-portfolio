# This is the original code for connecting an *actual* Atari Portfolio keyboard via FPC connector to a raspberry pi pico
# it is an 8 x 8 matrix connected with rows on GPIO1-8 and columns on 9-16

# This file is NOT needed for anything to do with the new PCB version... it is simply here as reference

import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

#optional delay before creating the HID for maximum compatibility
time.sleep(1)

#create the HID
kbd = Keyboard(usb_hid.devices)

#set up the row, column, and modifier arrays
rows = []
row_pins = [board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8]
for row in row_pins:
    row_key = digitalio.DigitalInOut(row)
    row_key.direction = digitalio.Direction.OUTPUT
    rows.append(row_key)

columns = []
column_pins = [board.GP9, board.GP10, board.GP11, board.GP12, board.GP13, board.GP14, board.GP15, board.GP16]
for column in column_pins:
    column_key = digitalio.DigitalInOut(column)
    column_key.direction = digitalio.Direction.INPUT
    column_key.pull = digitalio.Pull.DOWN
    columns.append(column_key)

#array of modifier keycodes
mod_keymap = [Keycode.LEFT_GUI,None,None,None,None,None,None,None,None,Keycode.LEFT_ALT,None,None,None,None,None,None,
            None,None,Keycode.LEFT_CONTROL,None,None,None,None,None,None,None,None,Keycode.LEFT_SHIFT,None,None,
            None,None,None,None,None,None,None,None,None,None,None,None,None,
            None,None,None,None,None,None,None,None,None,None,None,
            Keycode.F24,None,None,None,None,None,None,None,None,None]

#array of keycodes; if you want to remap see: https://circuitpython.readthedocs.io/projects/hid/en/latest/api.html#adafruit-hid-keycode-keycode /'None' values have no physical connection
keymap = [None,Keycode.DELETE,Keycode.TAB,Keycode.ZERO,Keycode.S,Keycode.F,Keycode.BACKSLASH,Keycode.C,None,None,Keycode.W,Keycode.I,Keycode.P,Keycode.H,Keycode.Z,Keycode.V,
            Keycode.ONE,Keycode.Q,None,Keycode.MINUS,Keycode.FOUR,Keycode.J,Keycode.SPACEBAR,Keycode.B,Keycode.TWO,Keycode.U,Keycode.E,None,Keycode.G,Keycode.LEFT_ARROW,
            Keycode.SEMICOLON,Keycode.N,Keycode.THREE,Keycode.O,Keycode.R,Keycode.LEFT_BRACKET,Keycode.RIGHT_SHIFT,Keycode.RIGHT_ARROW,Keycode.PERIOD,Keycode.M,Keycode.D,Keycode.SEVEN,Keycode.T,
            Keycode.UP_ARROW,Keycode.DOWN_ARROW,Keycode.CAPS_LOCK,Keycode.EQUALS,Keycode.FORWARD_SLASH,Keycode.FIVE,Keycode.BACKSPACE,Keycode.ENTER,Keycode.QUOTE,Keycode.COMMA,Keycode.EIGHT,
            None,Keycode.A,Keycode.SIX,Keycode.NINE,Keycode.Y,Keycode.RIGHT_BRACKET,Keycode.L,Keycode.K,Keycode.X,Keycode.ESCAPE]

def ProcessFunctionKey(key):
    print("Processing Fn")
    if(key == Keycode.ONE):
        return Keycode.F1
    elif(key == Keycode.TWO):
        return Keycode.F2
    elif(key == Keycode.TWO):
        return Keycode.F2
    elif(key == Keycode.THREE):
        return Keycode.F3
    elif(key == Keycode.FOUR):
        return Keycode.F4
    elif(key == Keycode.FIVE):
        return Keycode.F5
    elif(key == Keycode.SIX):
        return Keycode.F6
    elif(key == Keycode.SEVEN):
        return Keycode.F7
    elif(key == Keycode.EIGHT):
        return Keycode.F8
    elif(key == Keycode.NINE):
        return Keycode.F9
    else:
        return key

#main loop
while True:
    mod_keys = []
    reg_keys = []
    keypressed = False
    mod_keypressed = False

    for r in rows: #for each row
        r.value=1 #set row r to high
        for c in columns: #and then for each column
            if c.value: #if a keypress is detected (high row output --> switch closing circuit --> high column input)
                key = rows.index(r) * 8 + columns.index(c) #identify the key pressed via the index of the current row (r) and column (c)
                if mod_keymap[key] is not None:
                    mod_keypressed = True
                    mod_keys.append(mod_keymap[key])
                if keymap[key] is not None:
                    keypressed = True
                    reg_keys.append(keymap[key])
                    time.sleep(0.3) #delay a bit so that we don't get a load of duplicate presses

        r.value=0 #return the row to a low state, in preparation for the next row in the loop

    # Now instead of directly pressing the keys, we have stored them in arrays.
    # we must loop these and then press them.
    functionPressed = False
    if(len(mod_keys) > 0):
        for modifier_key in mod_keys:
            if modifier_key is Keycode.F24:
                functionPressed = True
            kbd.press(modifier_key)

    if(len(reg_keys) > 0):
        for reg_key in reg_keys:
            if functionPressed:
                kbd.press(ProcessFunctionKey(reg_key))
            else:
                kbd.press(reg_key)

        # once we are done and pressed everything in order, we can release all the keys
        kbd.release_all()

    if keypressed == False and mod_keypressed == False:
        kbd.release_all()

#TODO - CAPS LOCK TOGGLE
