# https://github.com/Saket-Upadhyay/PiPicoRFID

# MIT License

# Copyright (c) 2022 Saket Upadhyay

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import mfrc522
from os import uname

import utime

import machine
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

#Pin (6) is GP0 on Raspberry Pi Pico W (Rasp physical pin is 9)
#Pin (7) is GP1 on Raspberry Pi Pico W (Rasp physical pin is 10)

i2c = I2C(1, sda=machine.Pin(6), scl=machine.Pin(7), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)   

def RUN():
    print("Initialising Module=> " + str(uname()[0]))

    rdr = mfrc522.MFRC522(sck=2, miso=4, mosi=3, cs=1, rst=0)

    print("")
    print("Place card before reader. READ ARRD: 0x08")
    print("")

    try:
        while True:

            (stat, tag_type) = rdr.request(rdr.REQIDL)

            if stat == rdr.OK:

                (stat, raw_uid) = rdr.anticoll()

                if stat == rdr.OK:
                    print("CARD DETECTED")
                    print(" -  TAG TYPE : 0x%02x" % tag_type)
                    print(" -  UID      : 0x%02x%02x%02x%02x" %
                        (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print("")

                    if rdr.select_tag(raw_uid) == rdr.OK:

                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                        if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                            data = rdr.read(8)
                            datastr = ""
                            hexstr = []
                            for i in data:
                                datastr = datastr + (chr(i))
                                hexstr.append(hex(i))
                            print("DATA: " + str(datastr))
                            print("RAW DATA: " + str(hexstr))
                            # my custom display commands
                            # clear screen

                            lcd.clear()
                            lcd.move_to(5, 0)
                            lcd.putstr("Howdy")
                            lcd.move_to(2,1)
                            lcd.putstr("Sarayu Kochar!!")
                            utime.sleep(2)
                            rdr.stop_crypto1()
                        else:
                            print("AUTH ERR")
                    else:
                        print("Failed to select tag")

    except KeyboardInterrupt:
        print("EXITING PROGRAM")

if __name__=="__main__":
    RUN()


"""
from machine import Pin, SPI
import mfrc522

# Initialize SPI0
spi = SPI(0, baudrate=1000000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))

# Initialize the RFID reader
sda_pin = Pin(5)  # CS pin
rst_pin = Pin(6)  # RST pin
rfid = mfrc522.MFRC522(spi, sda_pin, rst_pin)

print("Place the card near the reader.")

while True:
    # Scan for cards
    (status, tag_type) = rfid.request(rfid.REQIDL)

    if status == rfid.OK:
        print("Card detected")
        
        # Get the card's UID
        (status, uid) = rfid.anticoll()
        
        if status == rfid.OK:
            print("Card UID:", uid)



---------------------------------------------------------

from mfrc522 import MFRC522
from time import sleep
from machine import Pin, PWM, I2C

# Define RFID RC522 pins
sck = Pin(6, Pin.OUT)
mosi = Pin(7, Pin.OUT)
miso = Pin(4, Pin.OUT)
rst = Pin(8, Pin.OUT)
sda = Pin(5, Pin.OUT)

# Initialize RC522
rfid_reader = MFRC522(sck, mosi, miso, rst, sda)

# Known valid RFID card UIDs (example UIDs in hexadecimal)
authorized_uids = [
    [0x12, 0x34, 0x56, 0x78],  # Example user 1
    [0x87, 0x65, 0x43, 0x21],  # Example user 2
]


# Function to authenticate users
def authenticate_user():
    print("Scan your RFID card...")
    while True:
        (status, tag_type) = rfid_reader.request(rfid_reader.REQIDL)
        if status == rfid_reader.OK:
            (status, uid) = rfid_reader.anticoll()
            if status == rfid_reader.OK:
                print("Card detected with UID:", uid)
                if uid in authorized_uids:
                    print("User authenticated!")
                    return True
                else:
                    print("Authentication failed. Try again.")
                    sleep(1)
        sleep(0.1)


# Main loop
while True:
    if authenticate_user():
        print ("User authenticated!")    
    else:
        print("Failed to authenticate!")
"""        

