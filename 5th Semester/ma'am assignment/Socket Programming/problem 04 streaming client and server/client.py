import socket
import subprocess
import threading
import time

HOST = '127.0.0.1'
PORT = 8000
BUFFER_SIZE = 10000

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

filename = input("Enter multimedia file to stream: ")
output_file = f"streaming_{filename}"

client.sendto(filename.encode(), (HOST, PORT))

response, _ = client.recvfrom(1024)
if response != b'OK':
    print("File not found on server")
    exit()

print("Streaming started...")

bytes_received = 0
player_launched = False

with open(output_file, 'wb') as f:
    while True:
        try:
            client.settimeout(2)
            data, _ = client.recvfrom(2048)
            
            if data == b'EOF':
                print("\nStreaming complete")
                break
            
            f.write(data)
            f.flush()
            bytes_received += len(data)
            print(f"Received: {bytes_received} bytes", end='\r')
            
            if bytes_received >= BUFFER_SIZE and not player_launched:
                print(f"\n{BUFFER_SIZE} bytes buffered. You can now play the file.")
                print(f"Run: vlc {output_file}  (or any media player)")
                player_launched = True
        
        except socket.timeout:
            print("\nStream timeout")
            break

print(f"File saved as: {output_file}")
client.close()
