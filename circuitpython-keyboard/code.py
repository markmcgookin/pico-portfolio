# Write your code here :-)
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

#this is 'overkill' for code consistency and hardware flexibility; you could alternatively connect modifiers directly to a constant high or low and read the switches without an enable/disable pin
modifier_enable = []
modifier_enable_pin = [board.GP22]
for mod in modifier_enable_pin:
    mod_enable = digitalio.DigitalInOut(mod)
    mod_enable.direction = digitalio.Direction.OUTPUT
    modifier_enable.append(mod_enable)

# modifiers = []
# modifier_pins = [board.GP17, board.GP18, board.GP19]
# for mod_pin in modifier_pins:
#     mod_key = digitalio.DigitalInOut(mod_pin)
#     mod_key.direction = digitalio.Direction.INPUT
#     mod_key.pull = digitalio.Pull.DOWN
#     modifiers.append(mod_key)

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

# TODO - MARKHERE:
# Find suitable map for Fn Key
# Special case/speedup backspace key
# Handle special case CAPS_LOCK toggle -> LED? Would be cool.
# Use the SSD1306 OLED?

def ProcessFunctionKey(key):
    print("Processing Fn")
    if(key == Keycode.ONE):
        print("F1")
        return Keycode.F1
    elif(key == Keycode.TWO):
        return Keycode.F2
    else:
        print("BASIC")
        return key
            
#main loop
while True:
    keypressed = False
    mod_keypressed = False
    mod_key = None
    for m_e in modifier_enable:
        m_e.value=1 #set the modifier pin to high
    for r in rows: #for each row
        r.value=1 #set row r to high
        for c in columns: #and then for each column
            if c.value: #if a keypress is detected (high row output --> switch closing circuit --> high column input)
                key = rows.index(r) * 8 + columns.index(c) #identify the key pressed via the index of the current row (r) and column (c)
                if mod_keymap[key] is not None:
                    mod_keypressed = True
                    mod_key = mod_keymap[key]
                    kbd.press(mod_key)
                    # don't release here so if we press this THEN a normal key later, it will still be pressed
                    
                if keymap[key] is not None:
                    print("KEY")
                    keyToPress = keymap[key]
                    keypressed = True
                    
                    if mod_keypressed is True: # OK this isn't working because in the same LOOP of the keyboard... we process the key press before the mod because it is earlier in the layout.
                                                # Need to cache all pressed keys until the end of the loop then press them.
                        print("MOD KEY")
                        if mod_key is Keycode.F24: # I am mapping this to the Fn Key as there isn't one in the Keycode library
                            print("F24")
                            keyToPress = ProcessFunctionKey(keymap[key])
                    
                    # if there is a key pressed, check to see if there is a modifier pin pressed too
                    kbd.press(keyToPress) #press the (non-modifier) key
                    kbd.release_all() #then release all keys pressed
                    time.sleep(0.3) #delay a bit so that we don't get a load of duplicate presses

        r.value=0 #return the row to a low state, in preparation for the next row in the loop
    
    if keypressed == False and mod_keypressed == False:
        # There are no keys pressed in this whole loop 
        # This could be called when a modifier was pressed, but then released
        #   before a normal key was pressed
        
        #print("No keys pressed")
        kbd.release_all() 