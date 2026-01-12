from machine import Pin
from mfrc522 import MFRC522
import time

# Pin configuration (adjust if wired differently)
SCK = 2
MOSI = 3
MISO = 4
#RST = 6
RST = 0
#CS  = 5
CS  = 1

#rdr = mfrc522.MFRC522(sck=2, miso=4, mosi=3, cs=1, rst=0)

# Initialize RFID reader
rfid = MFRC522(SCK, MOSI, MISO, RST, CS)

print("Place your card near the reader...")

while True:
    # Look for a card
    (stat, tag_type) = rfid.request(rfid.REQIDL)
    #print (stat, tag_type)

    if stat == rfid.OK:
        print("Card detected")

        # Get the UID of the card
        (stat, uid) = rfid.anticoll()
        if stat == rfid.OK:
            print("Card UID:", uid)

            # Select the scanned tag
            if rfid.select_tag(uid) == rfid.OK:
                print("Tag selected")

            # Halt PICC
            rfid.stop_crypto1()
    
    time.sleep(0.5)



