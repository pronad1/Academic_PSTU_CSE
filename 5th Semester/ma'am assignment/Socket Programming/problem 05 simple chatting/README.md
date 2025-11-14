# Simple Chat Application

## Files:
- `tcp_chat_server.py` - TCP chat server
- `tcp_chat_client.py` - TCP chat client
- `udp_chat_server.py` - UDP chat server
- `udp_chat_client.py` - UDP chat client

## How to Run:

### TCP Chat (Connection-oriented):
1. Run server: `python tcp_chat_server.py`
2. Run client: `python tcp_chat_client.py`
3. Type messages and press Enter
4. Press Ctrl+C to stop

### UDP Chat (Connectionless):
1. Run server: `python udp_chat_server.py`
2. Run client: `python udp_chat_client.py`
3. Type messages and press Enter (max 1000 chars)
4. Press Ctrl+C to stop

## Features:
- Turn-based messaging (send -> receive -> send)
- Press Enter to send message
- Press Ctrl+C to exit
- UDP limited to 1000 characters per message
