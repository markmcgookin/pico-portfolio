# This file was used to produce the mapping output while I figured out the original *real* atari portfolio keybaord matrix.
# While not perfect, it does produce an output that allowed me to figure out the original matrix and produce the other 'original-code' file
# for making an atari portfolio keyboard work with a pico as a usb keyboard.

# This file is NOT needed for anything to do with the new PCB version... it is simply here as reference

import time
import board
import digitalio
import supervisor

# Define the 16 GPIO pins (GP1 through GP16 as specified)
pins = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4,board.GP5,board.GP6, board.GP7,board.GP8,
    board.GP9, board.GP10, board.GP11, board.GP12, board.GP13, board.GP14, board.GP15, board.GP16, board.GP17, board.GP18]

# Initialize all pins as inputs with pull-down resistors
io_pins = []
for pin in pins:
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.INPUT
    io.pull = digitalio.Pull.DOWN
    io_pins.append(io)

def reset_pins():
    """Reset all pins to input with pull-down resistors"""
    for io in io_pins:
        io.direction = digitalio.Direction.INPUT
        io.pull = digitalio.Pull.DOWN

# List of keyboard keys to map - using user's updated list
key_list = [
    "MODIFIERKEY_LEFT_CTRL",
    "MODIFIERKEY_LEFT_SHIFT",
    "MODIFIERKEY_RIGHT_SHIFT",
    "MODIFIERKEY_LEFT_ALT",
    "MODIFIERKEY_GUI",
    "MODIFIERKEY_FN",
    "KEY_A",
    "KEY_B",
    "KEY_C",
    "KEY_D",
    "KEY_E",
    "KEY_F",
    "KEY_G",
    "KEY_H",
    "KEY_I",
    "KEY_J",
    "KEY_K",
    "KEY_L",
    "KEY_M",
    "KEY_N",
    "KEY_O",
    "KEY_P",
    "KEY_Q",
    "KEY_R",
    "KEY_S",
    "KEY_T",
    "KEY_U",
    "KEY_V",
    "KEY_W",
    "KEY_X",
    "KEY_Y",
    "KEY_Z",
    "KEY_1",
    "KEY_2",
    "KEY_3",
    "KEY_4",
    "KEY_5",
    "KEY_6",
    "KEY_7",
    "KEY_8",
    "KEY_9",
    "KEY_0",
    "KEY_MINUS",
    "KEY_EQUAL",
    "KEY_BACKSPACE",
    "KEY_ESC",
    "KEY_DELETE",
    "KEY_RIGHT",
    "KEY_LEFT",
    "KEY_UP",
    "KEY_DOWN",
    "KEY_SLASH",
    "KEY_PERIOD",
    "KEY_COMMA",
    "KEY_SEMICOLON",
    "KEY_QUOTE",
    "KEY_ENTER",
    "KEY_LEFT_BRACE",
    "KEY_RIGHT_BRACE",
    "KEY_BACKSLASH",
    "KEY_CAPS_LOCK",
    "KEY_TAB",
    "KEY_SPACE"
]

def detect_key_connection():
    """Detect which pins are connected when a key is pressed"""
    connections = []

    # Test each pin as an output
    for i in range(16):
        # Reset all pins
        reset_pins()

        # Set current pin as output HIGH
        io_pins[i].direction = digitalio.Direction.OUTPUT
        io_pins[i].value = True

        # Check all other pins as inputs
        for j in range(16):
            if i != j and io_pins[j].value:
                # A key is pressed connecting output i to input j
                connections.append((i, j))

        # Reset pin after testing
        reset_pins()

    return connections

def map_keyboard():
    """Guide user through mapping each key"""
    print("\n===== Keyboard QMK Mapping Tool =====")
    print("This tool will guide you through mapping each key.")
    print("For each key, press and hold the key, then press Enter to detect it.")
    print("Type 'x' and press Enter at any time to skip the current key.")
    print("For modifier keys like Fn, the connection will be stored for later use.")
    print("Press Enter again after a key is detected to continue.\n")

    # Store the mapping results
    key_mapping = {}
    row_pins = set()
    col_pins = set()

    # Special storage for modifier keys
    modifier_connections = {}

    # Map each key in the list
    for idx, key_name in enumerate(key_list):
        print(f"Press key: {key_name} (Key {idx+1}/{len(key_list)})")
        print("  (Press and hold key, then press Enter to detect)")
        print("  (Or type 'x' and press Enter to skip this key)")

        # Wait for user input
        response = input().strip().lower()

        if response == 'x':
            print(f"  Skipping {key_name}")
            continue

        # User pressed Enter, detect the key
        print("  Detecting key...")
        connections = detect_key_connection()

        if connections:
            # Filter out bidirectional connections
            filtered_connections = filter_bidirectional_connections(connections)

            print(f"  Detected {len(filtered_connections)} connections:")
            for i, conn in enumerate(filtered_connections):
                print(f"    {i+1}. GP{conn[0]+1} -> GP{conn[1]+1}")

            # If this is a modifier key, store its connection
            if key_name.startswith("MODIFIERKEY_"):
                if filtered_connections:
                    # Store this modifier for later reference
                    modifier_connections[key_name] = filtered_connections[0]
                    print(f"  Stored {key_name} connection for reference with other keys")

            # Let user select which connection to use if multiple are detected
            if len(filtered_connections) > 1:
                # Print info about which modifiers might be active
                if modifier_connections:
                    print("  Note: The following modifiers have been mapped:")
                    for mod_name, mod_conn in modifier_connections.items():
                        print(f"    - {mod_name}: GP{mod_conn[0]+1} -> GP{mod_conn[1]+1}")
                    print("  If you're pressing a modifier, its connection should appear above.")

                # Ask user to select which connection to use
                print("  Multiple connections detected. Which one should be used for this key?")
                valid_selection = False
                while not valid_selection:
                    try:
                        selection = input("  Enter number (1-{0}): ".format(len(filtered_connections)))
                        selection_idx = int(selection) - 1
                        if 0 <= selection_idx < len(filtered_connections):
                            conn = filtered_connections[selection_idx]
                            valid_selection = True
                        else:
                            print("  Invalid selection. Please try again.")
                    except ValueError:
                        print("  Please enter a number.")
            elif len(filtered_connections) == 1:
                # Only one connection, use it automatically
                conn = filtered_connections[0]
            else:
                print("  No valid connections detected. Press Enter to try again or 'x' to skip.")
                response = input().strip().lower()
                if response == 'x':
                    print(f"  Skipping {key_name}")
                    continue
                else:
                    # Try again with this key
                    idx -= 1
                    continue

            # Store the selected connection
            key_mapping[key_name] = conn

            # Track which pins are used as rows/columns
            row_pins.add(conn[0])
            col_pins.add(conn[1])

            # Continue to next key
            print("  Press Enter to continue to next key...")
            input()
        else:
            print("  No connections detected. Press Enter to try again or 'x' to skip.")
            response = input().strip().lower()
            if response == 'x':
                print(f"  Skipping {key_name}")
                continue
            else:
                # Try again with this key
                idx -= 1
                continue

    # Analyze results and generate QMK mapping
    print("\nMapping complete! Analyzing results...\n")

    # Sort rows and columns for consistent display
    rows = sorted(list(row_pins))
    cols = sorted(list(col_pins))

    # Print summary of mapped keys
    print("===== MAPPING SUMMARY =====")
    print(f"Total keys mapped: {len(key_mapping)}")
    print(f"Matrix dimensions: {len(rows)} rows × {len(cols)} columns")

    # Create a matrix to visualize the keyboard layout
    matrix = [[None for _ in range(len(cols))] for _ in range(len(rows))]

    # Fill the matrix with key names
    for key_name, (row_pin, col_pin) in key_mapping.items():
        if row_pin in rows and col_pin in cols:
            row_idx = rows.index(row_pin)
            col_idx = cols.index(col_pin)
            matrix[row_idx][col_idx] = key_name

    # Generate a CSV summary of the mapping
    print("\nMatrix CSV (for spreadsheet reference):")
    header = "," + ",".join([f"COL{i} (GP{cols[i]+1})" for i in range(len(cols))])
    print(header)

    for i, row in enumerate(matrix):
        row_values = []
        for key in row:
            row_values.append(key if key else "")
        print(f"ROW{i} (GP{rows[i]+1})," + ",".join(row_values))

    # Print which keys were mapped
    print("\nSuccessfully mapped keys:")
    for key_name in sorted(key_mapping.keys()):
        row_pin, col_pin = key_mapping[key_name]
        row_idx = rows.index(row_pin)
        col_idx = cols.index(col_pin)
        print(f"  - {key_name}: [Row {row_idx}, Col {col_idx}] (GP{row_pin+1} -> GP{col_pin+1})")

    # Print which keys were skipped
    skipped_keys = [key for key in key_list if key not in key_mapping]
    if skipped_keys:
        print("\nSkipped keys:")
        for key_name in skipped_keys:
            print(f"  - {key_name}")

    # Print a mapping file
    print("===== KEYBOARD MATRIX MAPPING =====\n\n")
    print(f"Matrix dimensions: {len(rows)} rows × {len(cols)} columns\n\n")

    print("QMK Matrix Definition:\n")
    print("```c\n")
    print(f"#define MATRIX_ROWS {len(rows)}\n")
    print(f"#define MATRIX_COLS {len(cols)}\n\n")
    print("#define MATRIX_ROW_PINS { " + ", ".join([f"GP{r+1}" for r in rows]) + " }\n")
    print("#define MATRIX_COL_PINS { " + ", ".join([f"GP{c+1}" for c in cols]) + " }\n")
    print("```\n\n")

    print("Key mapping:\n")
    print("```c\n")
    for key_name in sorted(key_mapping.keys()):
        row_pin, col_pin = key_mapping[key_name]
        row_idx = rows.index(row_pin)
        col_idx = cols.index(col_pin)
        print(f"#define {key_name} KEYMAP_POSITION({row_idx}, {col_idx})  // GP{row_pin+1} -> GP{col_pin+1}\n")
    print("```\n")

def filter_bidirectional_connections(connections):
    """Filter out bidirectional connections to avoid duplicates"""
    filtered = []
    seen = set()

    for conn in connections:
        # Check if the reverse connection has already been seen
        reverse_conn = (conn[1], conn[0])
        if reverse_conn not in seen:
            filtered.append(conn)
            seen.add(conn)

    return filtered

    # Determine row and column pins
    rows = sorted(list(row_pins))
    cols = sorted(list(col_pins))

    # Print detected matrix dimensions
    print(f"Detected matrix: {len(rows)} rows × {len(cols)} columns")
    print(f"Row pins: {['GP'+str(r+1) for r in rows]}")
    print(f"Column pins: {['GP'+str(c+1) for c in cols]}")

    # Generate QMK definitions
    print("\nQMK Matrix Definition:")
    print("```c")
    print("// Keyboard Matrix Dimensions")
    print(f"#define MATRIX_ROWS {len(rows)}")
    print(f"#define MATRIX_COLS {len(cols)}")
    print("")
    print("// Matrix Pin Connections")
    print("#define MATRIX_ROW_PINS { " + ", ".join([f"GP{r+1}" for r in rows]) + " }")
    print("#define MATRIX_COL_PINS { " + ", ".join([f"GP{c+1}" for c in cols]) + " }")
    print("```")

    # Generate keymap positions - using the exact key names provided
    print("\nKeymap Positions:")
    print("```c")
    print("// Key Matrix Position Reference for keymap.c")
    for key_name, (row_pin, col_pin) in sorted(key_mapping.items(), key=lambda x: x[0]):
        row_idx = rows.index(row_pin)
        col_idx = cols.index(col_pin)
        print(f"#define {key_name} KEYMAP_POSITION({row_idx}, {col_idx})")
    print("```")

    # Generate visual matrix
    print("\nVisual Matrix Layout:")
    matrix = [["." for _ in range(len(cols))] for _ in range(len(rows))]

    for key_name, (row_pin, col_pin) in key_mapping.items():
        row_idx = rows.index(row_pin)
        col_idx = cols.index(col_pin)
        matrix[row_idx][col_idx] = "X"

    # Print header
    header = "    " + " ".join([f"C{i}" for i in range(len(cols))])
    print(header)

    # Print each row
    for i, row in enumerate(matrix):
        print(f"R{i}  " + " ".join(row))

    # Generate key layout for keymap.c - using the exact key names
    print("\nSample keymap.c layout:")
    print("```c")
    print("[0] = LAYOUT(")

    # Create matrix of key names
    key_matrix = [[None for _ in range(len(cols))] for _ in range(len(rows))]
    for key_name, (row_pin, col_pin) in key_mapping.items():
        row_idx = rows.index(row_pin)
        col_idx = cols.index(col_pin)
        key_matrix[row_idx][col_idx] = key_name

    # Print rows
    for i, row in enumerate(key_matrix):
        row_str = "    "
        for j, key in enumerate(row):
            if key:
                # Use the exact key name format
                qmk_key = key
                row_str += qmk_key
            else:
                row_str += "KC_NO"

            if i < len(key_matrix) - 1 or j < len(row) - 1:
                row_str += ", "
        print(row_str)

    print(")")
    print("```")

# Run the mapping tool
map_keyboard()

print("\nMapping complete! You can now use these definitions in your QMK firmware.")
