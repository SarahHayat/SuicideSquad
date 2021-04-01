import socket
import struct
import time


s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.ntohs(0x0003))

test = []

while(1):
    now = time.time()
    message = s.recv(4096)
    print(message)
    # Process the message from here