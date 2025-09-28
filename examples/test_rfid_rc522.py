from machine import Pin
import mfrc522
import time

# ----------------------------
# Pin configuration (adjust if wired differently)
# ----------------------------
SCK  = 2   # SPI clock
MOSI = 3   # SPI MOSI
MISO = 4   # SPI MISO
CS   = 1   # SPI chip select (SDA)
RST  = 0   # Reset pin

# Initialize MFRC522
rfid = mfrc522.MFRC522(SCK, MOSI, MISO, RST, CS)

print("RFID reader initialized. Place a card near the reader.")

# ----------------------------
# Main loop: detect and print UID
# ----------------------------
while True:
    (status, tag_type) = rfid.request(rfid.REQIDL)
    if status == rfid.OK:
        (status, uid) = rfid.anticoll()
        if status == rfid.OK:
            # Print UID
            uid_str = "-".join("{:02X}".format(i) for i in uid)
            print("Card detected! UID:", uid_str)
            
            # Optional: select tag and stop crypto
            if rfid.select_tag(uid) == rfid.OK:
                rfid.stop_crypto1()
    
    time.sleep(0.5)

