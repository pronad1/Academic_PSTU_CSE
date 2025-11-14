import socket
import threading

HOST = '127.0.0.1'
PORT = 9500

def handle_client(conn, addr):
    print(f"[NEW] Client {addr} connected")
    try:
        while True:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"[{addr}] Client: {msg}")
            
            reply = input(f"[{addr}] You: ")
            conn.send(reply.encode())
    except:
        pass
    
    print(f"[DISCONNECTED] {addr}")
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Multi-Client Chat Server on {HOST}:{PORT}")
print("Waiting for clients...\n")

try:
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}\n")
except KeyboardInterrupt:
    print("\nServer stopped")

server.close()
