# SPDX-FileCopyrightText: 2023 Custom Keyboard Firmware
# SPDX-License-Identifier: MIT

import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Debug mode toggle - set to False for normal keyboard operation
# Set to True to only output to serial without sending keystrokes
DEBUG_MODE = True

# Initialize keyboard
keyboard = Keyboard(usb_hid.devices)

# Define pins for rows based on specified connections (top to bottom)
row_pins = [board.GP15, board.GP14, board.GP16, board.GP17, board.GP18]  # 5 rows

# Define pins for columns (left to right)
col_pins = [
    board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5,
    board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11,
    board.GP12, board.GP13  # 14 columns
]

# Setup rows as outputs with initial HIGH state
rows = []
for pin in row_pins:
    row = digitalio.DigitalInOut(pin)
    row.direction = digitalio.Direction.OUTPUT
    row.drive_mode = digitalio.DriveMode.PUSH_PULL
    row.value = True  # Set HIGH initially (inactive)
    rows.append(row)

# Setup columns as inputs with pull-up resistors
cols = []
for pin in col_pins:
    col = digitalio.DigitalInOut(pin)
    col.direction = digitalio.Direction.INPUT
    col.pull = digitalio.Pull.UP  # Pull-UP for diode-to-switch configuration
    cols.append(col)

# Define a dictionary to map keycode values to names
# This replaces the vars(Keycode) approach that's not available in CircuitPython
KEYCODE_NAMES = {
    Keycode.A: "A", Keycode.B: "B", Keycode.C: "C", Keycode.D: "D",
    Keycode.E: "E", Keycode.F: "F", Keycode.G: "G", Keycode.H: "H",
    Keycode.I: "I", Keycode.J: "J", Keycode.K: "K", Keycode.L: "L",
    Keycode.M: "M", Keycode.N: "N", Keycode.O: "O", Keycode.P: "P",
    Keycode.Q: "Q", Keycode.R: "R", Keycode.S: "S", Keycode.T: "T",
    Keycode.U: "U", Keycode.V: "V", Keycode.W: "W", Keycode.X: "X",
    Keycode.Y: "Y", Keycode.Z: "Z",
    Keycode.ONE: "1", Keycode.TWO: "2", Keycode.THREE: "3", Keycode.FOUR: "4",
    Keycode.FIVE: "5", Keycode.SIX: "6", Keycode.SEVEN: "7", Keycode.EIGHT: "8",
    Keycode.NINE: "9", Keycode.ZERO: "0",
    Keycode.ENTER: "ENTER", Keycode.RETURN: "RETURN", Keycode.ESCAPE: "ESC",
    Keycode.BACKSPACE: "BACKSPACE", Keycode.TAB: "TAB", Keycode.SPACEBAR: "SPACE",
    Keycode.SPACE: "SPACE", Keycode.MINUS: "MINUS", Keycode.EQUALS: "EQUALS",
    Keycode.LEFT_BRACKET: "LEFT_BRACKET", Keycode.RIGHT_BRACKET: "RIGHT_BRACKET",
    Keycode.BACKSLASH: "BACKSLASH", Keycode.SEMICOLON: "SEMICOLON",
    Keycode.QUOTE: "QUOTE", Keycode.GRAVE_ACCENT: "GRAVE",
    Keycode.COMMA: "COMMA", Keycode.PERIOD: "PERIOD", Keycode.FORWARD_SLASH: "SLASH",
    Keycode.CAPS_LOCK: "CAPS_LOCK",
    Keycode.F1: "F1", Keycode.F2: "F2", Keycode.F3: "F3", Keycode.F4: "F4",
    Keycode.F5: "F5", Keycode.F6: "F6", Keycode.F7: "F7", Keycode.F8: "F8",
    Keycode.F9: "F9", Keycode.F10: "F10", Keycode.F11: "F11", Keycode.F12: "F12",
    Keycode.PRINT_SCREEN: "PRINT_SCREEN", Keycode.SCROLL_LOCK: "SCROLL_LOCK",
    Keycode.PAUSE: "PAUSE", Keycode.INSERT: "INSERT", Keycode.HOME: "HOME",
    Keycode.PAGE_UP: "PAGE_UP", Keycode.DELETE: "DELETE", Keycode.END: "END",
    Keycode.PAGE_DOWN: "PAGE_DOWN", Keycode.RIGHT_ARROW: "RIGHT",
    Keycode.LEFT_ARROW: "LEFT", Keycode.DOWN_ARROW: "DOWN", Keycode.UP_ARROW: "UP",
    Keycode.KEYPAD_NUMLOCK: "NUM_LOCK", Keycode.KEYPAD_FORWARD_SLASH: "KP_SLASH",
    Keycode.KEYPAD_ASTERISK: "KP_ASTERISK", Keycode.KEYPAD_MINUS: "KP_MINUS",
    Keycode.KEYPAD_PLUS: "KP_PLUS", Keycode.KEYPAD_ENTER: "KP_ENTER",
    Keycode.KEYPAD_ONE: "KP_1", Keycode.KEYPAD_TWO: "KP_2", Keycode.KEYPAD_THREE: "KP_3",
    Keycode.KEYPAD_FOUR: "KP_4", Keycode.KEYPAD_FIVE: "KP_5", Keycode.KEYPAD_SIX: "KP_6",
    Keycode.KEYPAD_SEVEN: "KP_7", Keycode.KEYPAD_EIGHT: "KP_8", Keycode.KEYPAD_NINE: "KP_9",
    Keycode.KEYPAD_ZERO: "KP_0", Keycode.KEYPAD_PERIOD: "KP_PERIOD",
    Keycode.LEFT_CONTROL: "LEFT_CTRL", Keycode.LEFT_SHIFT: "LEFT_SHIFT",
    Keycode.LEFT_ALT: "LEFT_ALT", Keycode.LEFT_GUI: "LEFT_GUI",
    Keycode.RIGHT_CONTROL: "RIGHT_CTRL", Keycode.RIGHT_SHIFT: "RIGHT_SHIFT",
    Keycode.RIGHT_ALT: "RIGHT_ALT", Keycode.RIGHT_GUI: "RIGHT_GUI"
}

# Helper function to get keycode name from the Keycode value
def get_keycode_name(keycode_value):
    return KEYCODE_NAMES.get(keycode_value, f"UNKNOWN({keycode_value})")

# Define the keymap - 5 rows x 14 columns
# You can customize this with the specific keycodes you want for each position
keymap = [
    # Row 0 (top row)
    [Keycode.ESCAPE, Keycode.ONE, Keycode.TWO, Keycode.THREE, Keycode.FOUR, Keycode.FIVE,
     Keycode.SIX, Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE, Keycode.ZERO,
     Keycode.MINUS, Keycode.EQUALS, Keycode.BACKSPACE],

    # Row 1
    [Keycode.TAB, Keycode.Q, Keycode.W, Keycode.E, Keycode.R, Keycode.T,
     Keycode.Y, Keycode.U, Keycode.I, Keycode.O, Keycode.P,
     Keycode.LEFT_BRACKET, Keycode.RIGHT_BRACKET, Keycode.BACKSLASH],

    # Row 2
    [Keycode.CAPS_LOCK, Keycode.A, Keycode.S, Keycode.D, Keycode.F, Keycode.G,
     Keycode.H, Keycode.J, Keycode.K, Keycode.L, Keycode.SEMICOLON,
     Keycode.QUOTE, Keycode.ENTER, Keycode.DELETE],

    # Row 3
    [Keycode.LEFT_SHIFT, Keycode.Z, Keycode.X, Keycode.C, Keycode.V, Keycode.B,
     Keycode.N, Keycode.M, Keycode.COMMA, Keycode.PERIOD, Keycode.FORWARD_SLASH,
     Keycode.RIGHT_SHIFT, Keycode.UP_ARROW, Keycode.PAGE_UP],

    # Row 4 (bottom row)
    [Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.LEFT_GUI, Keycode.SPACE, Keycode.SPACE, Keycode.SPACE,
     Keycode.SPACE, Keycode.SPACE, Keycode.RIGHT_ALT, Keycode.RIGHT_CONTROL, Keycode.LEFT_ARROW,
     Keycode.DOWN_ARROW, Keycode.RIGHT_ARROW, Keycode.PAGE_DOWN]
]

# Keep track of the currently pressed keys
key_state = [[False for _ in range(len(col_pins))] for _ in range(len(row_pins))]

# Debounce time (in seconds)
DEBOUNCE_TIME = 0.01

# Last scan time for rate limiting
last_scan = time.monotonic()
scan_interval = 0.01  # 10ms between scans

print("Keyboard firmware initialized")
print(f"DEBUG MODE: {'ON' if DEBUG_MODE else 'OFF'}")
print(f"{'ONLY SERIAL OUTPUT' if DEBUG_MODE else 'NORMAL KEYBOARD OPERATION'}")

while True:
    current_time = time.monotonic()

    # Rate limiting to avoid overwhelming USB host
    if current_time - last_scan < scan_interval:
        continue

    last_scan = current_time

    # Scan the matrix
    for r in range(len(rows)):
        # Set current row LOW (active)
        rows[r].value = False
        time.sleep(0.001)  # Brief delay for electrical settling

        for c in range(len(cols)):
            # Read the column (LOW means key pressed with diode)
            key_pressed = not cols[c].value

            # Detect key state changes
            if key_pressed != key_state[r][c]:
                # Debounce
                time.sleep(DEBOUNCE_TIME)

                # Check again after debounce time
                key_pressed_debounced = not cols[c].value

                if key_pressed_debounced != key_state[r][c]:
                    # State has genuinely changed
                    key_state[r][c] = key_pressed_debounced
                    key_value = keymap[r][c]
                    key_name = get_keycode_name(key_value)

                    if key_pressed_debounced:
                        # Key pressed
                        print(f"Key pressed: Row {r}, Column {c} - {key_name}")

                        # Only send keystrokes if not in debug mode
                        if not DEBUG_MODE:
                            keyboard.press(key_value)
                    else:
                        # Key released
                        print(f"Key released: Row {r}, Column {c} - {key_name}")

                        # Only send keystrokes if not in debug mode
                        if not DEBUG_MODE:
                            keyboard.release(key_value)

        # Set row back to HIGH (inactive)
        rows[r].value = True
