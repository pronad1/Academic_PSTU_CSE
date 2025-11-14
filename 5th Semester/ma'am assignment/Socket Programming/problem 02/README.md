# Concurrent File Server

## Files:
- `server.py` - Multi-threaded file server
- `client.py` - File download client
- `sample.txt` - Test file

## How to Run:

1. Start server: `python server.py`
2. Run client(s): `python client.py`
3. Enter filename: `sample.txt`
4. File saved as `downloaded_sample.txt`

## Features:
- One thread per client connection
- 1000-byte chunks per transfer
- 200ms sleep after each flush
- Supports multiple concurrent clients
