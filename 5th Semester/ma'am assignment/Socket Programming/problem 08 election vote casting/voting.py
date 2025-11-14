import socket
import threading
import struct
import time

MCAST_GRP = '224.1.1.2'
MCAST_PORT = 5008
TOTAL_VOTERS = 5

votes = []
vote_lock = threading.Lock()

def receive_votes(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            vote = data.decode()
            
            with vote_lock:
                if vote in ['A', 'B']:
                    votes.append(vote)
                    print(f"\nVote received: {vote} (Total: {len(votes)}/{TOTAL_VOTERS})")
                    
                    if len(votes) == TOTAL_VOTERS:
                        display_result()
                        break
        except:
            break

def display_result():
    count_a = votes.count('A')
    count_b = votes.count('B')
    
    print("\n" + "="*40)
    print("ELECTION RESULTS")
    print("="*40)
    print(f"Candidate A: {count_a} votes")
    print(f"Candidate B: {count_b} votes")
    
    if count_a > count_b:
        print("\nWINNER: Candidate A")
    elif count_b > count_a:
        print("\nWINNER: Candidate B")
    else:
        print("\nRESULT: TIE")
    print("="*40)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))

mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print("Election Voting System")
print(f"Total Voters: {TOTAL_VOTERS}")
print("Candidates: A and B\n")

receiver = threading.Thread(target=receive_votes, args=(sock,))
receiver.daemon = True
receiver.start()

time.sleep(1)

while True:
    vote = input("Cast your vote (A or B): ").upper()
    if vote in ['A', 'B']:
        sock.sendto(vote.encode(), (MCAST_GRP, MCAST_PORT))
        print("Vote cast successfully!")
        break
    else:
        print("Invalid vote! Please enter A or B")

receiver.join()
sock.close()
