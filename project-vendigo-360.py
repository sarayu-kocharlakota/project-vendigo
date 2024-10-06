# This code works with continuous servo motor
# TD-8125MG 25KG Digital Servo 360 Degree Waterproof Large Torque Metal Gear
# for DIY Robot Robotic Arm RC Model PWM 500μs-2500μs
# https://www.amazon.com/dp/B08JCT4P3B?ref=ppx_yo2ov_dt_b_fed_asin_title


from machine import Pin, PWM
import utime
import mfrc522
from os import uname
import utime
#import machine
from machine import I2C, Pin, PWM
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# 16x2 LCD connections
# Pin 38 - GND - GND pin of LCD 
# Pin 40 - VBUS - VCC pin of LCD
# Pin 9 -  GP6  - SDA pin of LCD
# Pin 10 - GP7 - SCL pin of LCD


# RFID -RC522 connections
# Pin 2 -  GP1 - SDA pin of RFID-RC522 connected to GP1 (Pin 2) or SPI0 CSn of Raspberry Pi Pico W 
# Pin 4 -  GP2 - SCK pin of RFID-RC522 connected to GP2 (Pin 4) or SPI0 SCK of Raspberry Pi Pico W 
# Pin 5 -  GP3 - MOSI pin of RFID-RC522 connected to GP3 (Pin 5) or SPI0 TX of Raspberry Pi Pico W 
# Pin 6 -  GP4 - MISO pin of RFID-RC522 connected to GP4 (Pin 6) or SPI0 RX of Raspberry Pi Pico W 
#          NONE- IRQ pin of RFID-RC522 to no pin of Raspberry Pi Pico W 
# Pin 3 -  GND pin of RFID-RC522 connected to GND (Pin 3) of Raspberry Pi Pico W 
# Pin 1 -  GP0 - RST pin of RFID-RC522 connected to GP0 (Pin 1) or SPI0 SCK of Raspberry Pi Pico W 
# Pin 36 - 3V3 OUT - 3.3V pin of RFID-RC522 connected to 3V3 (OUT) (Pin 36) of Raspberry Pi Pico W


# 4x4 Matrix Keyboard connections
# Pin 11 - GP8 - Pin 1 of 4x4 Row 1
# Pin 12 - GP9 - Pin 2 of 4x4 Row 2
# Pin 14 - GP10 - Pin 3 of 4x4 Row 3
# Pin 15 - GP11 - Pin 4 of 4x4 Row 4
# Pin 16 - GP12 - Pin 5 of 4x4 Col 1
# Pin 17 - GP13 - Pin 6 of 4x4 Col 2
# Pin 19 - GP14 - Pin 7 of 4x4 Col 3
# Pin 20 - GP15 - Pin 8 of 4x4 Col 4

# Continuous Servo (360 degrees) Motor connections
# Pin 28 - Orange wire: This is generally the signal wire. It receives the PWM (Pulse Width Modulation)
# signal that controls the servo's rotation. Connect this wire to your PWM pin (like Pin 28 in your setup).

# Positive (RED Wire) Goes to + of the External Power Supply
# Red wire: This is typically the power supply wire (positive, or VCC).
# It connects to the power source, usually 5V or 6V, depending on the servo's specifications.

# Brown wire: This is usually the ground wire (GND). It should be connected to the ground
# of power supply or controller.

# 270 degree Servo Motor
# Red (in both cases) is the power wire (VCC).
# Orange (new motor) replaces the white (old motor) as the signal wire.
# Brown (new motor) replaces the black (old motor) as the ground wire.

I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(1, sda=machine.Pin(6), scl=machine.Pin(7), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# 4x4 Matrix Keypad Configuration
ROWS = [Pin(8, Pin.IN, Pin.PULL_DOWN), Pin(9, Pin.IN, Pin.PULL_DOWN), Pin(10, Pin.IN, Pin.PULL_DOWN), Pin(11, Pin.IN, Pin.PULL_DOWN)]
COLS = [Pin(12, Pin.OUT), Pin(13, Pin.OUT), Pin(14, Pin.OUT), Pin(15, Pin.OUT)]
keys = [['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']]

# Map UIDs to names
UID_MAP = {
    b'\x93\x5e\xdf\xd9': "Sarayu Kochar",
    b'\xcc\x00\x33\x02': "Harsha Halvi",
    b'\xe3\xfc\xb6\xd9': "Sindhu Halvi",
    b'\x12\x58\x32\x02': "Sridhar Kochar",
    b'\xc3\x9c\xd1\xd9': "Subbarao K V",
    b'\xaa\x1c\x34\x02': "Srinu Kochar",
}

# Function to get name from UID
def get_name_from_uid(raw_uid):
    uid_bytes = bytes(raw_uid[:4])  # Use first 4 bytes
    return UID_MAP.get(uid_bytes, "Unknown")

# Debouncing function for the keypad
def scan_keypad():
    for col in range(4):
        for c in range(4):
            COLS[c].low()
        COLS[col].high()
        for row in range(4):
            if ROWS[row].value() == 1:
                utime.sleep(0.3)  # Debounce delay
                return keys[row][col]
    return None

# Function to center text on LCD
def center_text_on_lcd(text, row):
    text = text[:16]  # Ensure the text doesn't exceed the display width
    spaces = (16 - len(text)) // 2
    lcd.move_to(spaces, row)
    lcd.putstr(text)

# Servo Configuration
servo_pin = Pin(28)
servo = PWM(servo_pin)
servo.freq(50)

# Map 500us (full CCW) to 2500us (full CW) to duty_u16 values
def servo_duty_from_us(us):
    return int(us / 20000 * 65535)

# Function to stop the 360-degree servo
def stop_servo():
    servo.duty_u16(servo_duty_from_us(1500))  # Neutral position (1500us pulse)

# Function to rotate precisely and stop with minimal overshoot
def rotate_360_cw():
    print("Rotating 360 degrees clockwise...")
    
    # 2500us pulse width for full speed clockwise
    servo.duty_u16(servo_duty_from_us(2500))
    
    # Rotate for a slightly shorter duration, then stop briefly
    rotation_time = 1  # Start with slightly less than the full time
    utime.sleep(rotation_time)
    
    # Stop the motor momentarily to prevent overshoot
    stop_servo()
    utime.sleep(0.05)  # Brief stop, can adjust this as well

    # Small correction to get it to the exact position
    #servo.duty_u16(servo_duty_from_us(2500))  # Brief clockwise nudge
    #utime.sleep(0.05)  # Small additional rotation

    #stop_servo()  # Final stop
    print("Rotation complete. Servo stopped.")


# Replace the 270 degree rotation with continuous rotation
def vend_item():
    print("Vending item!")
    lcd.clear()
    lcd.move_to(2, 0)
    lcd.putstr("Vending item!")

    # Rotate clockwise for a specific time to simulate 360-degree rotation
    rotate_360_cw()  # Full speed clockwise
    utime.sleep(1)  # Adjust time based on how long it takes to rotate 360 degrees

    stop_servo()  # Stop the motor after vending
    utime.sleep(0.5)  # Pause before resetting

    lcd.clear()
    lcd.move_to(5, 0)
    lcd.putstr("Enjoy!!")
    utime.sleep(0.5)
    #lcd.clear()

# Replace set_angle(270) with vend_item()
def RUN():
    print("Initialising Module=> " + str(uname()[0]))
    rdr = mfrc522.MFRC522(sck=2, miso=4, mosi=3, cs=1, rst=0)

    lcd.clear()
    print("\nPlace card before reader.\n")

    star_counter = 0  # Counter for '*' key presses

    try:
        while True:
            # Check if a card is placed before the reader
            lcd.move_to(1, 0)
            lcd.putstr("PROJECT VENDIGO")
            lcd.move_to(0, 1)
            lcd.putstr("Please scan card")

            (stat, tag_type) = rdr.request(rdr.REQIDL)
            if stat == rdr.OK:
                (stat, raw_uid) = rdr.anticoll()
                if stat == rdr.OK:
                    name = get_name_from_uid(raw_uid)
                    print(f"CARD DETECTED: {name}")

                    if name != "Unknown":
                        lcd.clear()
                        lcd.move_to(5, 0)
                        lcd.putstr("Howdy")
                        lcd.move_to(2,1)
                        lcd.putstr(name)

                        utime.sleep(1.5)
                        lcd.clear()
                        center_text_on_lcd("SELECT ITEM:", 0)
                        
                        input_string = ""

                        while True:
                            key = scan_keypad()
                            if key:
                                # Handle double '*' press to clear the system
                                if key == '*':
                                    star_counter += 1
                                    if star_counter == 2:
                                        print("Double '*' detected, resetting...")
                                        lcd.clear()
                                        star_counter = 0
                                        break  # Exit the inner loop, waiting for a new RFID scan
                                else:
                                    star_counter = 0  # Reset the counter if any other key is pressed

                                # If user presses '#', finalize input
                                if key == '#':
                                    if input_string == "1A":
                                        vend_item()  # Call the function to rotate 360 degrees
                                    else:
                                        lcd.clear()
                                        #lcd.putstr("Invalid Item!")
                                        center_text_on_lcd("Invalid Item!", 0)
                                        center_text_on_lcd("Scan Again!", 1)
                                        #utime.sleep(0.75)
                                        #lcd.clear()
                                        #lcd.putstr("Scan Again!")
                                        utime.sleep(1.25)
                                    utime.sleep(2)  # Wait before resetting
                                    lcd.clear()
                                    break  # Exit the loop and wait for the next scan
                                else:
                                    input_string += key
                                    print(f"Current input: {input_string}")
                                    lcd.clear()
                                    center_text_on_lcd("SELECT ITEM:", 0)  # Keep the first line
                                    center_text_on_lcd(input_string, 1)        # Display user input in the center of the second line

            utime.sleep(0.5)

    except KeyboardInterrupt:
        print("Exiting program")
        stop_servo()  # Ensure the servo stops when the program is interrupted

if __name__ == "__main__":
    RUN()

