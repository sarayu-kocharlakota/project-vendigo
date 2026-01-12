from machine import Pin
import time

# Define the rows and columns of the keypad
ROWS = [Pin(8, Pin.IN, Pin.PULL_DOWN), Pin(9, Pin.IN, Pin.PULL_DOWN), Pin(10, Pin.IN, Pin.PULL_DOWN), Pin(11, Pin.IN, Pin.PULL_DOWN)]
COLS = [Pin(12, Pin.OUT), Pin(13, Pin.OUT), Pin(14, Pin.OUT), Pin(15, Pin.OUT)]

# Key mapping of the 4x4 keypad
keys = [['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']]

input_string = ""  # to store the input
final_string = ""  # to store the final result after # is pressed

# Function to scan the keypad and return the pressed key
def scan_keypad():
    for col in range(4):
        # Set all columns to high
        for c in range(4):
            COLS[c].low()
        # Set the current column to low
        COLS[col].high()

        # Check if any row is pressed
        for row in range(4):
            if ROWS[row].value() == 1:  # key is pressed
                time.sleep(0.1)  # debounce delay
                return keys[row][col]
    return None

# Main loop to capture input
try:
    while True:
        key = scan_keypad()

        if key:
            if key == '#':
                final_string = input_string  # finalize the input
                print("Final input: ", final_string)
                input_string = ""  # reset for next input
            else:
                input_string += key  # accumulate the input
                print("Current input: ", input_string)

        time.sleep(0.1)  # polling delay

except KeyboardInterrupt:
    print("Exiting program")

