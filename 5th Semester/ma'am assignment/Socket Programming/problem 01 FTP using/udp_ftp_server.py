import socket

HOST = '127.0.0.1'
PORT = 5001

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print(f"UDP Server listening on {HOST}:{PORT}")

with open('received_file_udp.txt', 'w') as f:
    while True:
        data, addr = server.recvfrom(1024)
        if data == b'EOF':
            print("File transfer complete")
            break
        line = data.decode()
        f.write(line)
        print(f"Received: {line.strip()}")

server.close()
