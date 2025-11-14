import socket

HOST = '127.0.0.1'
PORT = 9000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print(f"Connected to TCP Chat Server\n")

try:
    while True:
        msg = input("You: ")
        client.send(msg.encode())
        
        reply = client.recv(1024).decode()
        if not reply:
            break
        print(f"Server: {reply}")
except KeyboardInterrupt:
    print("\nChat ended")

client.close()
