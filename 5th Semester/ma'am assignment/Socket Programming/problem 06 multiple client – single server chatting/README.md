# Multi-Client Chat Server

## Files:
- `server.py` - Multi-threaded chat server
- `client.py` - Chat client

## How to Run:

1. Start server: `python server.py`
2. Run multiple clients: `python client.py` (run in separate terminals)
3. Server shows client address for each message
4. Type messages and press Enter
5. Press Ctrl+C to stop

## Features:
- Server handles multiple clients simultaneously
- One thread per client connection
- Turn-based messaging per client
- Each client chats independently with server

## Example:
Terminal 1: `python server.py`
Terminal 2: `python client.py`
Terminal 3: `python client.py`
Terminal 4: `python client.py`
