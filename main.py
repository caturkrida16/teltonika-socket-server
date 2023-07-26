# TASK BERFORE RUN THIS PROGRAM
"""
1. 
"""

### >>><<< ###
# Packages
## System
import socket
import threading
import binascii

## PIP
from twos_complement import twos_complement

### >>><<< ###
# Intialization
SERVER = "0.0.0.0"
PORT = 9797

### >>><<< ###
# Core
## Function
### Decode the Data
def decodethis(data):
    # Get the Codec Data
    codec = int(data[16:18], 16)
    
    if (codec == 8):
        length = int(data[8:16], 16)
        record = int(data[18:20], 16)
        timestamp = int(data[20:36], 16)
        priority = int(data[36:38], 16)
        longitude = int(data[38:46], 16)
        latitude = int(data[46:54], 16)
        altitude = int(data[54:58], 16)
        angle = int(data[58:62], 16)
        satellites = int(data[62:64], 16)
        speed = int(data[64:68], 16)
        
        # Convert the Integer Location to Longitude and Latitude format
        longitude = loc_convert(longitude)
        latitude = loc_convert(latitude)
        
        print("Length: " + str(length))
        print("Record: " + str(record))
        print("Timestamp: " + str(timestamp))
        print("Priority: " + str(priority))
        print("Latitude: " + str(latitude))
        print("Longitude: " + str(longitude))
        print("Altitude: " + str(altitude))
        print("Angle: " + str(angle))
        print("Satellites: " + str(satellites))
        print("Speed: " + str(speed))
        print("")

        # You need to send the record data back in total 4 bytes
        return record.to_bytes(4, 'big')

### Location converter
def loc_convert(loc):
    # Get the max data integer in 31 bit.
    check = 2 ** 31
    
    # 10 ** 7 or 10e7 is from Teltonika website
    # If data not bigger than 2e31, just divide with 10e7
    # Than if data bigger than 2e31, convert location to binary and do 2's complement. After that divide with 10e7 and multiply with -1
    if (loc < check):
        loc_int = float(loc) / 10 ** 7
        return loc_int
        
    elif (loc > check):
        loc_bin = bin(loc).replace("0b", "")
        loc_bin = twos_complement(loc_bin)
        loc_int = float(int(loc_bin, 2)) / 10 ** 7
        return loc_int * -1
    
    elif (loc == 0):
        return "0"

### Handle the Client
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    imei = conn.recv(1280)
    imei = imei.decode()
    print("IMEI: " + imei[2:26])
    message = '\x01'
    message = message.encode('utf-8')
    conn.send(message)
    
    while connected:
        try:
            data = conn.recv(1280)
            recieved = binascii.hexlify(data)
            record = decodethis(recieved)
            conn.send(record)

        except socket.error:
            print("Error Occured.")
            break

    conn.close()

### Start the server
def start():
    s.listen()
    print("Server is listening ...")

    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

## Main
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER, PORT))
print("[STARTING] server is starting...")
start()
