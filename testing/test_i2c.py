from machine import Pin, I2C
import utime

i2c = I2C(1, sda=Pin(6), scl=Pin(7), freq=400000)

print("Scanning I2C bus...")
devices = i2c.scan()

if not devices:
    print("No I2C devices found!")
else:
    print("I2C devices found:", [hex(d) for d in devices])
