from machine import Pin, PWM
import time

servo = PWM(Pin(15))  # change to your pin
servo.freq(50)

def set_servo(pulse):
    duty = int((pulse / 20000) * 65535)
    servo.duty_u16(duty)

# Sweep test
for pulse in range(1000, 2001, 50):  # reverse → forward
    set_servo(pulse)
    time.sleep(0.1)

set_servo(1500)  # stop
