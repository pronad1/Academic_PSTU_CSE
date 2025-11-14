import socket

HOST = '127.0.0.1'
PORT = 9000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"TCP Chat Server waiting on {HOST}:{PORT}")
conn, addr = server.accept()
print(f"Connected to {addr}\n")

try:
    while True:
        msg = conn.recv(1024).decode()
        if not msg:
            break
        print(f"Client: {msg}")
        
        reply = input("You: ")
        conn.send(reply.encode())
except KeyboardInterrupt:
    print("\nChat ended")

conn.close()
server.close()
