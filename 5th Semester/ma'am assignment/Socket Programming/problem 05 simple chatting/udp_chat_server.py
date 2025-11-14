import socket

HOST = '127.0.0.1'
PORT = 9001

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print(f"UDP Chat Server waiting on {HOST}:{PORT}\n")

try:
    while True:
        msg, addr = server.recvfrom(1000)
        print(f"Client: {msg.decode()}")
        
        reply = input("You: ")
        server.sendto(reply.encode(), addr)
except KeyboardInterrupt:
    print("\nChat ended")

server.close()
