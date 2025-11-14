import socket
import threading
import time
import os

HOST = '127.0.0.1'
PORT = 6000

def handle_client(conn, addr):
    print(f"Thread started for client {addr}")
    
    filename = conn.recv(1024).decode()
    print(f"Client {addr} requested: {filename}")
    
    if os.path.exists(filename):
        conn.send(b'OK')
        with open(filename, 'rb') as f:
            while True:
                data = f.read(1000)
                if not data:
                    break
                conn.send(data)
                time.sleep(0.2)
        print(f"File {filename} sent to {addr}")
    else:
        conn.send(b'ERROR: File not found')
    
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"Server listening on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print(f"Connection from {addr}")
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
