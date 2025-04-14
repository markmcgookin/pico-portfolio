# Write your code here :-)
import board
import digitalio
import time

# Array of strings to print
messages = [
    "a",
    "b",
    "c",
    "d"
]

# Set up buttons connected to GPIO pins 1-16
buttons = []
for pin_number in range(1, 17):
    pin_name = None
    # Try different pin naming conventions
    try:
        pin = getattr(board, "GP" + str(pin_number))  # For Raspberry Pi Pico
        pin_name = "GP" + str(pin_number)
    except AttributeError:
        try:
            pin = getattr(board, "D" + str(pin_number))  # For Feather, ItsyBitsy
            pin_name = "D" + str(pin_number)
        except AttributeError:
            try:
                pin = getattr(board, "IO" + str(pin_number))  # For ESP32
                pin_name = "IO" + str(pin_number)
            except AttributeError:
                print("Warning: Could not find pin", pin_number, "skipping")
                continue

    button = digitalio.DigitalInOut(pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP  # Using pull-up resistors
    buttons.append((pin_number, button))
    print("Added button on pin", pin_name)

print("Button detector initialized with", len(buttons), "buttons")

def wait_for_button_release():
    """Wait until all buttons are released"""
    print("Waiting for buttons to be released...")
    all_released = False
    while not all_released:
        all_released = True
        for pin_num, button in buttons:
            if not button.value:  # Button is still pressed (remember we're using pull-up)
                all_released = False
                break
        time.sleep(0.1)
    print("All buttons released")

def get_pressed_buttons_for_duration(duration_seconds):
    """
    Wait for buttons to be pressed and held for the specified duration.
    Returns a list of pin numbers that were held down for the full duration.
    """
    print("Waiting for buttons to be pressed and held for", duration_seconds, "seconds...")

    # Wait for at least one button to be pressed
    any_pressed = False
    while not any_pressed:
        for _, button in buttons:
            if not button.value:  # Button is pressed (LOW with pull-up)
                any_pressed = True
                print("button pressed")  # Print once when a button is detected
                break
        time.sleep(0.1)

    # Record which buttons are initially pressed
    button_press_start = {}
    for pin_num, button in buttons:
        if not button.value:  # Button is pressed (LOW with pull-up)
            button_press_start[pin_num] = time.time()

    # Continue monitoring until the required duration has passed
    end_time = time.time() + duration_seconds

    # Keep track of which buttons were held for the full duration
    buttons_held = []
    for pin_num in button_press_start:
        buttons_held.append(pin_num)

    while time.time() < end_time and len(buttons_held) > 0:
        for i in range(len(buttons_held) - 1, -1, -1):
            pin_num = buttons_held[i]
            # Find the button object for this pin
            for btn_pin, btn in buttons:
                if btn_pin == pin_num:
                    # If button was initially pressed but now released, remove from held list
                    if btn.value:
                        buttons_held.pop(i)
                    break
        time.sleep(0.1)

    return buttons_held

# Main loop to go through each message
message_index = 0
while message_index < len(messages):
    message = messages[message_index]
    print("\n" + message)

    # Wait for button press and hold
    pressed_pins = get_pressed_buttons_for_duration(5)

    if pressed_pins:
        print("Buttons held for 5 seconds:", pressed_pins)
        # Only increment to next message after successful 5-second hold
        message_index += 1
    else:
        print("No buttons were held for the full 5 seconds. Try again.")
        # Don't increment message_index, we'll repeat this message

    # Wait for all buttons to be released before continuing
    wait_for_button_release()

print("All messages processed. Program complete.")
