from machine import Pin, PWM
import time

# Set up the PWM pin
servo_pin = Pin(28)  # Change this to the pin you're using
servo = PWM(servo_pin)

# Set the frequency to 50 Hz
servo.freq(50)

# Function to set the angle of the servo
def set_angle(angle):
    # Map the angle (0-270) to pulse width (500-2500 μs)
    pulse_width = int((angle / 270) * (2500 - 500) + 500)
    servo.duty_u16(int(pulse_width * 65535 / 20000))  # Convert to duty cycle

# Test the servo
try:
    while True:
        for angle in range(0, 271, 10):  # Move from 0 to 270 degrees
            set_angle(angle)
            time.sleep(0.1)
        for angle in range(270, -1, -10):  # Move back to 0 degrees
            set_angle(angle)
            time.sleep(0.1)
except KeyboardInterrupt:
    servo.duty_u16(0)  # Stop the servo when interrupted
    servo.deinit()

