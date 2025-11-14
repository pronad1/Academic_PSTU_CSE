import socket

HOST = '127.0.0.1'
PORT = 6000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

filename = input("Enter filename to download: ")
client.send(filename.encode())

response = client.recv(1024)
if response == b'OK':
    with open(f'downloaded_{filename}', 'wb') as f:
        while True:
            data = client.recv(1000)
            if not data:
                break
            f.write(data)
    print(f"File downloaded as downloaded_{filename}")
else:
    print(response.decode())

client.close()
