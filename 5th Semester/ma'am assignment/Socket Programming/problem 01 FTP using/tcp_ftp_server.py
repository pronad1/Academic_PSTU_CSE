import socket

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"TCP Server listening on {HOST}:{PORT}")

conn, addr = server.accept()
print(f"Connected by {addr}")

with open('received_file.txt', 'wb') as f:
    while True:
        data = conn.recv(100)
        if not data:
            break
        f.write(data)
        conn.send(b'ACK')
        print(f"Received {len(data)} bytes, sent ACK")

print("File transfer complete")
conn.close()
server.close()
