# Simple FTP Implementation

## Files:
- `tcp_ftp_server.py` - TCP server (connection-oriented)
- `tcp_ftp_client.py` - TCP client (connection-oriented)
- `udp_ftp_server.py` - UDP server (connectionless)
- `udp_ftp_client.py` - UDP client (connectionless)
- `testfile.txt` - Sample file for testing

## How to Run:

### TCP FTP (Connection-Oriented):
1. Run server: `python tcp_ftp_server.py`
2. Run client: `python tcp_ftp_client.py`
3. Enter filename: `testfile.txt`
4. File saved as `received_file.txt`

### UDP FTP (Connectionless):
1. Run server: `python udp_ftp_server.py`
2. Run client: `python udp_ftp_client.py`
3. Enter filename: `testfile.txt`
4. File saved as `received_file_udp.txt`

## Features:
- **TCP**: 100-byte chunks, ACK-based, timeout & retransmission
- **UDP**: Line-by-line transfer, no ACK required
