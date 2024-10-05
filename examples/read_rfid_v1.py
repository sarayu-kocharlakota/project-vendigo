from machine import Pin, SPI
from mfrc522 import MFRC522

# Initialize SPI0
spi = SPI(0, baudrate=1000000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3), miso=Pin(4))

# Initialize RFID reader
rfid = MFRC522(spi, sck=2, mosi=3, miso=4, cs=5, rst=6)

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

