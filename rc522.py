Python 3.10.10 (tags/v3.10.10:aad5f6a, Feb  7 2023, 17:20:36) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import RPi.GPIO as GPIO
... import MFRC522
... import signal
... 
... continue_reading = True
... 
... # Capture SIGINT for cleanup when the script is aborted
... def end_read(signal, frame):
...     global continue_reading
...     print("Ctrl+C captured, ending read.")
...     continue_reading = False
...     GPIO.cleanup()
... 
... # Hook the SIGINT
... signal.signal(signal.SIGINT, end_read)
... 
... # Create an object of the class MFRC522
... MIFAREReader = MFRC522.MFRC522()
... 
... def read_card():
...     # Scan for cards    
...     (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
... 
...     # If a card is found
...     if status == MIFAREReader.MI_OK:
...         print("Card detected")
...     
...     # Get the UID of the card
...     (status, uid) = MIFAREReader.MFRC522_Anticoll()
... 
...     # If we have the UID, continue
...     if status == MIFAREReader.MI_OK:
... 
...         # Print UID
...         print("Card read UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3]))
...     
...         # This is the default key for authentication
...         key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
...         
...         # Select the scanned tag
...         MIFAREReader.MFRC522_SelectTag(uid)
... 
...         # Authenticate
...         status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
... 
...         # Check if authenticated
...         if status == MIFAREReader.MI_OK:
...             # Read block 8
...             data = MIFAREReader.MFRC522_Read(8)
...             print("Data read from block 8: " + str(data))
... 
... def write_card():
...     # Scan for cards    
...     (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
... 
...     # If a card is found
...     if status == MIFAREReader.MI_OK:
...         print("Card detected")
...     
    # Get the UID of the card
    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print("Card read UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3]))
    
        # This is the default key for authentication
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        
def write_data(block_number, data):
    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block_number, key, uid)
    if status == MIFAREReader.MI_OK:
        MIFAREReader.MFRC522_Write(block_number, data)
        print("Data written successfully.")
    else:
        print("Authentication error.")

def read_data(block_number):
    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block_number, key, uid)
    if status == MIFAREReader.MI_OK:
        data = MIFAREReader.MFRC522_Read(block_number)
        print("Data read: " + ''.join([chr(x) for x in data]))
    else:
        print("Authentication error.")

def copy_card(from_block, to_block):
    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, from_block, key, uid)
    if status == MIFAREReader.MI_OK:
        data = MIFAREReader.MFRC522_Read(from_block)
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, to_block, key, uid)
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Write(to_block, data)
            print("Card copied successfully.")
        else:
            print("Authentication error while writing to target card.")
    else:
        print("Authentication error while reading source card.")

while continue_reading:
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    if status == MIFAREReader.MI_OK:
        print("Card detected.")
        (status, uid) = MIFAREReader.MFRC522_Anticoll()

        if status == MIFAREReader.MI_OK:
            print("Card UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3]))

            while True:
                print("1. Write data")
                print("2. Read data")
                print("3. Copy card")
                print("4. Exit")
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    block_number = int(input("Enter block number: "))
                    data = input("Enter data: ")
                    data = list(data.ljust(16, ' '))
                    write_data(block_number, data)
                elif choice == 2:
                    block_number = int(input("Enter block number: "))
                    read_data(block_number)
                elif choice == 3:
                    from_block = int(input("Enter source block number: "))
                    to_block = int(input("Enter target block number: "))
                    copy_card(from_block, to_block)
                elif choice == 4:
                    break
                else:
                    print("Invalid choice.")
