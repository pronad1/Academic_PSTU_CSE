import socket
import threading
import struct

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

def receive_messages(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            msg = data.decode()
            print(f"\n[{addr[0]}:{addr[1]}] {msg}")
            print("You: ", end='', flush=True)
        except:
            break

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))

mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print("Multicast Chat started")
print(f"Group: {MCAST_GRP}:{MCAST_PORT}\n")

receiver = threading.Thread(target=receive_messages, args=(sock,))
receiver.daemon = True
receiver.start()

try:
    while True:
        msg = input("You: ")
        sock.sendto(msg.encode(), (MCAST_GRP, MCAST_PORT))
except KeyboardInterrupt:
    print("\nChat ended")

sock.close()
