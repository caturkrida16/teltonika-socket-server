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

        return record.to_bytes(4, 'big')

### Location converter
def loc_convert(loc):
    loc_int = float(loc)
    loc_bin = bin(loc).replace("0b", "")
    if (loc_bin[0:1] == 0):
        loc_int = loc_int / 10000000
        return loc_int
        
    if (loc_bin[0:1] == 1):
        loc_bin = twos_complement(loc_bin)
        loc_int = float(int(loc_bin, 2)) / 10000000
        return loc_int

### Handle the Client
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    imei = conn.recv(1024)
    message = '\x01'
    message = message.encode('utf-8')
    conn.send(message)
    
    while connected:
        try:
            data = conn.recv(1024)
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
