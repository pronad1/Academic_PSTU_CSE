import socket
import random
import os
import time

HOST = '127.0.0.1'
PORT = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print(f"Streaming Server listening on {HOST}:{PORT}")

while True:
    data, addr = server.recvfrom(1024)
    filename = data.decode()
    print(f"Client {addr} requested: {filename}")
    
    if os.path.exists(filename):
        server.sendto(b'OK', addr)
        time.sleep(0.1)
        
        with open(filename, 'rb') as f:
            while True:
                chunk_size = random.randint(1000, 2000)
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                server.sendto(chunk, addr)
                print(f"Sent {len(chunk)} bytes to {addr}")
                time.sleep(0.05)
        
        server.sendto(b'EOF', addr)
        print(f"Streaming complete for {filename}")
    else:
        server.sendto(b'ERROR', addr)
        print(f"File not found: {filename}")