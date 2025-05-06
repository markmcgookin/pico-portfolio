import board
import digitalio
import time

# This just scans the 5 x 14 matrix on the pico portfolio and confirms that all the buttons are working when you press them

# Define pins for rows based on your specified connections (top to bottom)
row_pins = [board.GP15, board.GP14, board.GP16, board.GP17, board.GP18]  # 5 rows
row_names = ["GP15", "GP14", "GP16", "GP17", "GP18"]

# Define pins for columns (left to right)
col_pins = [
    board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5,
    board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11,
    board.GP12, board.GP13  # 14 columns
]
col_names = ["GP0", "GP1", "GP2", "GP3", "GP4", "GP5", "GP6", "GP7",
             "GP8", "GP9", "GP10", "GP11", "GP12", "GP13"]

# Setup rows as outputs with initial HIGH state
rows = []
for pin in row_pins:
    row = digitalio.DigitalInOut(pin)
    row.direction = digitalio.Direction.OUTPUT
    row.drive_mode = digitalio.DriveMode.PUSH_PULL
    row.value = True  # Set HIGH initially (this is important for the diode matrix)
    rows.append(row)

# Setup columns as inputs with pull-up resistors
cols = []
for pin in col_pins:
    col = digitalio.DigitalInOut(pin)
    col.direction = digitalio.Direction.INPUT
    col.pull = digitalio.Pull.UP  # Pull-UP is critical for diode-to-switch configuration
    cols.append(col)

def debug_matrix():
    """Test each position in the matrix and report results."""
    print("Starting keyboard matrix debug...")
    print("Testing each row and column intersection...")

    for r in range(len(rows)):
        # Set current row LOW (active) - all other rows stay HIGH
        rows[r].value = False
        time.sleep(0.02)  # Small delay for stability

        # Check each column in this row - should read LOW when pressed due to diode
        for c in range(len(cols)):
            if not cols[c].value:  # Note the NOT here - we're looking for LOW
                print(f"Button detected at row {r} ({row_names[r]}), column {c} ({col_names[c]})")

        # Set row back to HIGH (inactive)
        rows[r].value = True
        time.sleep(0.02)  # Small delay before next row

def test_individual_pins():
    """Test each pin individually to ensure they're working."""
    print("\nTesting individual row pins...")

    # First ensure all rows are HIGH
    for r in range(len(rows)):
        rows[r].value = True

    # Now test each row by setting it LOW and checking columns
    for r in range(len(rows)):
        print(f"Setting Row {r} ({row_names[r]}) LOW - pressing keys in this row should register")
        rows[r].value = False
        time.sleep(0.5)

        # Check if any buttons are pressed in this row
        for c in range(len(cols)):
            if not cols[c].value:
                print(f"  Detected: Row {r} ({row_names[r]}), Column {c} ({col_names[c]})")

        rows[r].value = True
        time.sleep(0.2)

    print("\nColumn input test:")
    # Test each column input independently
    for c in range(len(cols)):
        print(f"Column {c} ({col_names[c]}) reading: {cols[c].value}")

# Basic connection test
print("Performing basic connection test...")
for c in range(len(cols)):
    if not cols[c].value:
        print(f"WARNING: Column {c} ({col_names[c]}) is reading LOW without any rows active!")

# Main loop
while True:
    print("\n--- Keyboard Matrix Debug (Diode-to-Switch Config) ---")
    print("Row mapping: 0=GP15, 1=GP14, 2=GP16, 3=GP17, 4=GP18")
    print("Column mapping: 0-13 = GP0-GP13")
    print("Logic: Rows default HIGH, set LOW to activate. Columns read LOW when pressed.")
    print("Press Ctrl+C to exit")

    # Run the debug function
    debug_matrix()

    # Test individual pins
    test_individual_pins()

    # Interactive test mode
    print("\nInteractive test mode: Press keys to see detection")
    try:
        timeout = time.time() + 10  # 10-second timeout
        print(f"Running for {timeout - time.time():.1f} seconds...")
        while time.time() < timeout:
            for r in range(len(rows)):
                rows[r].value = False  # Set row LOW (active)
                for c in range(len(cols)):
                    if not cols[c].value:  # Note the NOT - we're looking for LOW
                        print(f"Key pressed: Row {r} ({row_names[r]}), Column {c} ({col_names[c]})")
                        time.sleep(0.1)  # Debounce
                rows[r].value = True  # Set row back to HIGH (inactive)
    except KeyboardInterrupt:
        break

    print("Waiting 5 seconds before next scan...")
    time.sleep(5)# Write your code here :-)
