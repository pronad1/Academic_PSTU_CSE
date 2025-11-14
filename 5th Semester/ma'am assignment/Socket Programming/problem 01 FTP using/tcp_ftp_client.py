import socket
import time

HOST = '127.0.0.1'
PORT = 5000
TIMEOUT = 2

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.settimeout(TIMEOUT)

filename = input("Enter filename to send: ")

with open(filename, 'rb') as f:
    while True:
        chunk = f.read(100)
        if not chunk:
            break
        
        ack_received = False
        while not ack_received:
            try:
                client.send(chunk)
                print(f"Sent {len(chunk)} bytes")
                
                ack = client.recv(1024)
                if ack == b'ACK':
                    print("ACK received")
                    ack_received = True
            except socket.timeout:
                print("Timeout! Retransmitting...")

print("File transfer complete")
client.close()
