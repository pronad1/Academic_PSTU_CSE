# Multicast Group Chat

## Files:
- `multicast_chat.py` - Multicast chat application

## How to Run:

1. Run multiple instances: `python multicast_chat.py`
2. Open 3-4 terminals and run the same command in each
3. Type messages and press Enter
4. All group members receive the message
5. Press Ctrl+C to exit

## Features:
- Multicast group communication (224.1.1.1:5007)
- Send messages to all group members simultaneously
- Receive messages from any group member
- Each process can send/receive unlimited messages
- Shows sender's IP and port with each message

## Example:
Terminal 1: `python multicast_chat.py`
Terminal 2: `python multicast_chat.py`
Terminal 3: `python multicast_chat.py`

All terminals will see messages from all others.
