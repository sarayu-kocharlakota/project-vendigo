import mfrc522
from os import uname
import utime
import machine
from machine import I2C, Pin, PWM
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# Constants
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
SERVO_PIN    = 28  # Change this to the pin you're using
SERVO_MIN    = 500  # Minimum pulse width in μs
SERVO_MAX    = 2500 # Maximum pulse width in μs
ITEMS = {
    "1A": 270,  # Add more items as needed
}

# Initialize I2C and LCD
i2c = I2C(1, sda=machine.Pin(6), scl=machine.Pin(7), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Initialize Servo
servo = PWM(Pin(SERVO_PIN))
servo.freq(50)

# Function to set the angle of the servo
def set_angle(angle):
    pulse_width = int((angle / 270) * (SERVO_MAX - SERVO_MIN) + SERVO_MIN)
    servo.duty_u16(int(pulse_width * 65535 / 20000))

# Map UIDs to names
UID_MAP = {
    b'\x93\x5e\xdf\xd9': "Sarayu Kochar",
    b'\xcc\x00\x33\x02': "Sree Koch",
    b'\xe3\xfc\xb6\xd9': "Sindhu Halvi",
    b'\x12\x58\x32\x02': "Halvi Raya",
    b'\xc3\x9c\xd1\xd9': "Subbarao K V",
    b'\xaa\x1c\x34\x02': "Harsha Halvi",
}

def get_name_from_uid(raw_uid):
    return UID_MAP.get(bytes(raw_uid), "Unknown")

# Keypad scanning functionality
ROWS = [Pin(8, Pin.IN, Pin.PULL_DOWN), Pin(9, Pin.IN, Pin.PULL_DOWN), Pin(10, Pin.IN, Pin.PULL_DOWN), Pin(11, Pin.IN, Pin.PULL_DOWN)]
COLS = [Pin(12, Pin.OUT), Pin(13, Pin.OUT), Pin(14, Pin.OUT), Pin(15, Pin.OUT)]

# Key mapping of the 4x4 keypad
keys = [['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']]

def scan_keypad():
    for col in range(4):
        for c in range(4):
            COLS[c].low()
        COLS[col].high()
        for row in range(4):
            if ROWS[row].value() == 1:  # key is pressed
                utime.sleep(0.1)  # debounce delay
                return keys[row][col]
    return None

def RUN():
    print("Initialising Module=> " + str(uname()[0]))
    rdr = mfrc522.MFRC522(sck=2, miso=4, mosi=3, cs=1, rst=0)
    
    print("")
    print("Place card before reader.")
    print("")

    try:
        while True:
            (stat, tag_type) = rdr.request(rdr.REQIDL)
            if stat == rdr.OK:
                (stat, raw_uid) = rdr.anticoll()
                if stat == rdr.OK:
                    name = get_name_from_uid(raw_uid)
                    print("CARD DETECTED: ", name)
                    lcd.clear()
                    lcd.putstr("Howdy " + name)
                    utime.sleep(3)
                    
                    lcd.clear()
                    lcd.putstr("Pls select your item:")
                    utime.sleep(1)

                    input_string = ""  # to store the input
                    while True:
                        key = scan_keypad()
                        if key:
                            if key == '#':
                                final_string = input_string
                                print("Final input: ", final_string)
                                input_string = ""  # reset for next input
                                if final_string in ITEMS:
                                    angle = ITEMS[final_string]
                                    set_angle(angle)
                                    lcd.clear()
                                    lcd.putstr("Vending item! Enjoy!")
                                else:
                                    lcd.clear()
                                    lcd.putstr("Invalid Item!")
                                utime.sleep(3)
                                lcd.clear()
                                lcd.putstr("Pls select your item:")
                                break  # break to wait for the next RFID scan
                            else:
                                input_string += key
                                print("Current input: ", input_string)
            utime.sleep(0.1)  # Polling delay

    except KeyboardInterrupt:
        print("EXITING PROGRAM")
        servo.duty_u16(0)  # Stop the servo when interrupted
        servo.deinit()

if __name__=="__main__":
    RUN()

