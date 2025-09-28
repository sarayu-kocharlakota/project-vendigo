# https://github.com/T-622/RPI-PICO-I2C-LCD

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

i2c = I2C(0, sda=machine.Pin(6), scl=machine.Pin(7), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)    

# my custom display commands
# clear screen

lcd.clear()
lcd.move_to(5, 0)
lcd.putstr("Howdy")
lcd.move_to(2,1)
lcd.putstr("Sarayu Kochar!!")
utime.sleep(2)


