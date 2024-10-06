# project-vendigo

## Raspberry Pi Pico W Pin Connections for LCD, RFID, 4x4 Matrix Keypad, and Servo Motors

This README describes the pin configuration of the Raspberry Pi Pico W and its connections to various peripherals like a 16x2 LCD display, RFID-RC522 module, 4x4 Matrix Keypad, and continuous rotation servo motors.

## Table of Connections

| **Peripheral**     | **Raspberry Pi Pico Pin** | **GPIO Pin Name** | **Peripheral Pin**                | **Description**                                |
|--------------------|---------------------------|-------------------|-----------------------------------|------------------------------------------------|
| **16x2 LCD**       | Pin 38                    | GND               | GND                              | Ground connection for LCD                      |
|                    | Pin 40                    | VBUS              | VCC                              | Power (VCC) connection for LCD                 |
|                    | Pin 9                     | GP6               | SDA                              | Serial Data Line for LCD (I2C interface)       |
|                    | Pin 10                    | GP7               | SCL                              | Serial Clock Line for LCD (I2C interface)      |
| **RFID-RC522**     | Pin 2                     | GP1               | SDA                              | Serial Data Line for RFID (SPI0 CSn)           |
|                    | Pin 4                     | GP2               | SCK                              | Serial Clock for RFID (SPI0 SCK)               |
|                    | Pin 5                     | GP3               | MOSI                             | Master Out Slave In for RFID (SPI0 TX)         |
|                    | Pin 6                     | GP4               | MISO                             | Master In Slave Out for RFID (SPI0 RX)         |
|                    | Pin 3                     | GND               | GND                              | Ground connection for RFID                     |
|                    | Pin 1                     | GP0               | RST                              | Reset pin for RFID                             |
|                    | Pin 36                    | 3V3 OUT           | 3.3V                             | Power connection for RFID                      |
| **4x4 Matrix Keypad** | Pin 11                  | GP8               | Row 1                            | Connection to Row 1 of Keypad                  |
|                    | Pin 12                    | GP9               | Row 2                            | Connection to Row 2 of Keypad                  |
|                    | Pin 14                    | GP10              | Row 3                            | Connection to Row 3 of Keypad                  |
|                    | Pin 15                    | GP11              | Row 4                            | Connection to Row 4 of Keypad                  |
|                    | Pin 16                    | GP12              | Col 1                            | Connection to Column 1 of Keypad               |
|                    | Pin 17                    | GP13              | Col 2                            | Connection to Column 2 of Keypad               |
|                    | Pin 19                    | GP14              | Col 3                            | Connection to Column 3 of Keypad               |
|                    | Pin 20                    | GP15              | Col 4                            | Connection to Column 4 of Keypad               |
| **Continuous Servo**| Pin 28                    | GP28              | Orange wire                      | PWM signal for controlling servo rotation      |
|                    | External Power Supply      | N/A               | Red wire                         | Power (VCC) connection for the servo           |
|                    | Ground (GND)              | N/A               | Brown wire                       | Ground connection for the servo                |

## Power Supply Notes

- The RFID-RC522 is powered by the 3.3V pin of the Raspberry Pi Pico W.
- The continuous rotation servo motor requires an external power supply. Connect the servo's positive (red) wire to the positive terminal of the external power supply, and the ground (brown) wire to the ground terminal.

## Additional Notes

- The RFID-RC522 module uses SPI communication, which requires configuring the correct pins for SPI0 on the Raspberry Pi Pico W.
- The 16x2 LCD uses the I2C protocol and is connected via the SDA and SCL lines.
- The 4x4 Matrix Keypad is connected to a set of GPIO pins (GP8–GP15) for scanning the row and column inputs.
- Ensure that the servos are properly powered with a separate power supply if needed, as the Raspberry Pi Pico W might not supply enough current to drive multiple motors.

## References

- [Raspberry Pi Pico Documentation](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf)
- [RFID-RC522 Module Documentation](https://www.nxp.com/docs/en/data-sheet/MFRC522.pdf)
- [4x4 Matrix Keypad Datasheet](https://www.sparkfun.com/datasheets/Components/General/COM-14662_4x4_Matrix_Keypad.pdf)
