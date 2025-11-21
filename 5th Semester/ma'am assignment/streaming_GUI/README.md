# 🎬 UDP Media Streaming Application

A professional connectionless socket-based multimedia streaming application built with Python and Tkinter.

## 📋 Project Overview

This application demonstrates UDP-based streaming of multimedia files between a server and client. The server reads files in randomly distributed chunk sizes (1000-2000 bytes) and transmits them as UDP datagrams. The client receives these packets and can begin playback before the download completes.

### ✨ Key Features

#### Server Features
- 🎥 **File Selection**: Browse and select any audio or video file
- 📊 **Real-time Monitoring**: Live connection status and transfer statistics
- 📝 **Detailed Logging**: Timestamped event logs with progress tracking
- 🔄 **Multiple Connections**: Handle multiple client requests
- 🎲 **Random Packet Sizing**: Automatic randomization between 1000-2000 bytes
- 💻 **Professional GUI**: Modern, user-friendly interface

#### Client Features
- 🌐 **Network Configuration**: Connect to any server IP and port
- 📥 **Download Management**: Real-time progress with speed statistics
- ▶️ **Auto-playback**: Automatic media player launch when ready
- 📁 **Custom Save Location**: Choose where to save downloaded files
- ⏯️ **Progressive Playback**: Start viewing/listening while downloading
- 📊 **Progress Tracking**: Visual progress bar with detailed statistics

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Windows/Linux/macOS

### Installation

1. Clone or download this repository
2. No additional packages required (uses Python standard library)

### Running the Application

#### Option 1: Main Launcher (Recommended)
```bash
python main_gui.py
```
This launches a professional interface where you can choose to run the server or client.

#### Option 2: Direct Launch

**Server:**
```bash
python server.py
```

**Client:**
```bash
python client.py
```

## 📖 Complete Step-by-Step Process

### 🎯 **SCENARIO 1: Testing on Same Computer (Easiest)**

#### Step 1: Open the Main Application
```bash
python main_gui.py
```
You'll see a window with two big buttons:
- 📤 **"I Want to SHARE"** (for sending files)
- 📥 **"I Want to RECEIVE"** (for downloading files)

#### Step 2: Start the Server (Sharing Side)
1. Click **"I Want to SHARE"** button
2. A new window opens titled "📤 Share Your Files"
3. Follow the 3 steps shown:

   **STEP 1: Choose Your File 📁**
   - Click **"📂 SELECT FILE"** button
   - Browse and select any video (.mp4, .avi, .mkv) or audio (.mp3, .wav) file
   - You'll see the filename and size displayed

   **STEP 2: Start Sharing ▶️**
   - Leave the port as default (10000)
   - Click **"✅ START SHARING NOW"** button
   - Status will change to **"🟢 Sharing Active"**

   **STEP 3: Monitor Activity 📊**
   - Watch the log window for connection messages
   - You'll see when someone connects and downloads

#### Step 3: Start the Client (Receiving Side)
1. Go back to the main window
2. Click **"I Want to RECEIVE"** button
3. A new window opens titled "📥 Receive & Download Files"
4. Follow the 3 steps shown:

   **STEP 1: Enter Server Details 🔗**
   - Server IP: Keep as **"localhost"** (since same computer)
   - Port: Keep as **"10000"** (default)
   - See the helpful tip: "💡 Same computer? Use 'localhost'"

   **STEP 2: Choose Where to Save 💾**
   - Default location is shown (downloads folder)
   - Click **"Change Folder"** if you want different location

   **STEP 3: Start Download & Watch Progress 📊**
   - Make sure **"✓ Auto-play when enough downloaded"** is checked
   - Click **"✅ START DOWNLOAD NOW"** button
   - Watch the progress bar fill up
   - See download speed, percentage, and time remaining
   - Media player will **automatically open** when 100 KB is downloaded
   - You can **watch/listen while it's still downloading!**

#### Step 4: Enjoy!
- The file plays automatically
- Download continues in background
- When complete, you'll see "Download completed!" message
- File is saved in your downloads folder

---

### 🌐 **SCENARIO 2: Sharing Between Two Computers**

#### On the SERVER Computer (Person Sharing):

1. **Find Your IP Address First:**
   ```bash
   ipconfig    # On Windows
   ifconfig    # On Linux/Mac
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

2. **Start the Application:**
   ```bash
   python main_gui.py
   ```

3. **Set Up Sharing:**
   - Click **"I Want to SHARE"**
   - Select your file (Step 1)
   - Click **"START SHARING NOW"** (Step 2)
   - **Tell the other person your IP address** (e.g., 192.168.1.100)

4. **Wait for Connection:**
   - Keep the window open
   - Watch the log - you'll see when they connect
   - Watch the progress as file uploads

#### On the CLIENT Computer (Person Receiving):

1. **Start the Application:**
   ```bash
   python main_gui.py
   ```

2. **Set Up Receiving:**
   - Click **"I Want to RECEIVE"**
   - **IMPORTANT:** In "Server IP Address", enter the IP you got from sender
     - Example: Change "localhost" to **"192.168.1.100"**
   - Keep port as "10000"
   - Click **"START DOWNLOAD NOW"**

3. **Download & Enjoy:**
   - Watch progress bar
   - File plays automatically when ready
   - Continue watching while downloading

---

### 🔄 **SCENARIO 3: Multiple People Downloading**

The server can handle multiple clients at once!

**Server (One Person):**
- Set up once as shown above
- Keep it running

**Clients (Multiple People):**
- Each person clicks **"I Want to RECEIVE"**
- Everyone enters the same server IP
- Everyone can download simultaneously
- Each gets their own copy

---

### ⚙️ **Advanced Options**

#### Server Options:
- **Change Port:** If 10000 is busy, try 10001, 10002, etc.
- **Clear Log:** Click "🗑 Clear Log" to clean the activity window
- **Stop Sharing:** Click "⬛ STOP SHARING" when done

#### Client Options:
- **Auto-play:** Uncheck to download without playing
- **Save Location:** Click "Change Folder" to pick where files go
- **Stop Download:** Click "⬛ STOP DOWNLOAD" to cancel
- **Manual Play:** Click "▶️ PLAY FILE" after download completes

---

### 🎬 **Quick Start Summary**

**Same Computer Testing:**
```
1. Run: python main_gui.py
2. Click "I Want to SHARE" → Select file → Start Sharing
3. Click "I Want to RECEIVE" → Keep "localhost" → Start Download
4. Watch it work! File plays automatically
```

**Different Computers:**
```
SERVER: Get IP → Share file → Give IP to others
CLIENT: Enter server IP → Start download → Enjoy!
```

---

### 💡 **What You'll See**

#### In Server Window:
- ✅ "File selected: movie.mp4 (45.5 MB)"
- ✅ "Server bound to 0.0.0.0:10000"
- ✅ "Connection from 192.168.1.105"
- ✅ "Sent metadata to client"
- ✅ "Progress: 25.5% (11,500,000/45,000,000 bytes)"
- ✅ "Completed: Sent 45,000,000 bytes"

#### In Client Window:
- ✅ "Connecting to 192.168.1.100:10000..."
- ✅ "Receiving: movie.mp4"
- ✅ "File size: 45.50 MB"
- ✅ Progress bar filling up
- ✅ "35.2% - 15.80/45.50 MB - 384 KB/s - ETA: 78s"
- ✅ "Buffer threshold reached (100 KB)"
- ✅ "Launching media player..."
- ✅ "✓ Download completed successfully!"

---

### 🎓 **For Your Lab Demonstration**

**Demo Flow (8 minutes):**

1. **Introduction (1 min):** Explain UDP streaming concept

2. **Show Main Interface (1 min):**
   - Simple choice: Share or Receive
   - Clear instructions

3. **Server Setup (2 min):**
   - Click "I Want to SHARE"
   - Show 3-step process
   - Select file.mp4
   - Start server
   - Point out real-time logging

4. **Client Connection (2 min):**
   - Click "I Want to RECEIVE"
   - Use localhost for demo
   - Start download
   - Show progress bar, speed stats

5. **Progressive Playback (1 min):**
   - File starts playing automatically
   - Still downloading in background
   - This is the key feature!

6. **Q&A (1 min):**
   - Answer questions about UDP, packets, etc.

**Key Points to Mention:**
- ✅ Uses UDP (connectionless sockets)
- ✅ Random packet sizes 1000-2000 bytes
- ✅ Progressive playback while downloading
- ✅ User-friendly interface with clear steps
- ✅ Real-time progress and statistics

## 🔧 Configuration

Edit `config.py` to customize:

- **Network Settings**: Default IP, port, timeouts
- **Packet Settings**: Min/max packet sizes, buffer sizes
- **Playback Settings**: Buffer threshold, auto-play behavior
- **UI Settings**: Window dimensions, update intervals

## 📁 Project Structure

```
streaming_GUI/
├── main_gui.py          # Main launcher interface
├── server.py            # UDP streaming server
├── client.py            # UDP streaming client
├── config.py            # Configuration settings
├── README.md            # This file
└── downloads/           # Default download directory (created automatically)
```

## 🎯 Technical Details

### How It Works (Behind the Scenes)

#### 1. **Connection Initiation**
```python
# Client sends request to server
client_socket.sendto(b'START_STREAM', (server_ip, port))
```
- Client creates UDP socket
- Sends "START_STREAM" message to server
- Server receives request and prepares to send file

#### 2. **Metadata Exchange**
```python
# Server sends file information
metadata = f"{filename}|{file_size}".encode()
server_socket.sendto(metadata, client_address)
```
- Server sends filename and total size
- Client receives and displays this info
- Client prepares to receive data

#### 3. **Data Transfer (Random Packet Sizes)**
```python
# Server reads and sends random-sized chunks
chunk_size = random.randint(1000, 2000)  # Random between 1000-2000 bytes
chunk = file.read(chunk_size)
server_socket.sendto(chunk, client_address)
```
- Server opens the media file
- For each packet:
  - Randomly determines size (1000-2000 bytes)
  - Reads that many bytes from file
  - Sends as UDP datagram
  - Adds small delay (0.01s) to simulate streaming
- Last packet can be less than 1000 bytes (whatever remains)

#### 4. **Client Reception**
```python
# Client receives and saves data
data, _ = client_socket.recvfrom(2048)
file.write(data)
bytes_received += len(data)
```
- Client receives each UDP packet
- Writes data to file immediately
- Tracks total bytes received
- Updates progress bar and statistics

#### 5. **Progressive Playback**
```python
# Launch player when buffer threshold reached
if bytes_received >= 100*1024 and not playback_started:
    launch_media_player()
    playback_started = True
```
- Client monitors bytes received
- When 100 KB reached (configurable):
  - Launches system media player
  - Player opens the partially downloaded file
  - User can watch/listen while download continues

#### 6. **Completion**
```python
# Server sends end marker
server_socket.sendto(b"EOF", client_address)
```
- When file fully sent, server sends "EOF" marker
- Client receives EOF and closes file
- Download complete message shown

### Why UDP? (Connectionless Sockets)

**UDP Characteristics:**
- ✅ No connection establishment (faster)
- ✅ No handshake overhead
- ✅ Lower latency
- ✅ Suitable for streaming
- ⚠️ No guaranteed delivery (acceptable for media)

**Comparison:**
```
TCP:                          UDP:
[SYN] → ← [SYN-ACK] → [ACK]  [DATA] → (No handshake)
Connection setup              Immediate transmission
Slower start                  Faster start
Reliable delivery             Best-effort delivery
```

### Packet Size Randomization

**Why Random?**
```python
chunk_size = random.randint(1000, 2000)
```
- Simulates real-world network conditions
- Tests robustness of implementation
- Meets project requirements (1000-2000 bytes)
- Last packet naturally becomes < 1000 if file ends

**Example Transmission:**
```
Packet 1: 1847 bytes
Packet 2: 1203 bytes
Packet 3: 1965 bytes
Packet 4: 1450 bytes
...
Packet N: 892 bytes (last packet, < 1000 OK!)
EOF marker
```

### Multi-Threading Architecture

```
Main GUI Thread
│
├─ Server Thread (listens for requests)
│  └─ Client Handler Thread 1 (sends to client A)
│  └─ Client Handler Thread 2 (sends to client B)
│  └─ Client Handler Thread 3 (sends to client C)
│
└─ Client Thread (receives and writes data)
   └─ Media Player (separate process)
```

**Benefits:**
- GUI stays responsive
- Multiple simultaneous downloads
- Non-blocking operations

### Real-Time Statistics

**Client Calculates:**
```python
speed = bytes_received / elapsed_time / 1024  # KB/s
progress = (bytes_received / file_size) * 100  # Percentage
remaining = (file_size - bytes_received) / (speed * 1024)  # Seconds
```

**Display Shows:**
- Progress: "45.2%"
- Downloaded: "20.5 / 45.5 MB"
- Speed: "384 KB/s"
- ETA: "65 seconds"

## 🎓 Academic Context & Requirements

### Lab Assignment Requirements

**Original Assignment:**
> Develop a streaming client and server application using connectionless sockets that works as follows: The streaming client contacts the streaming server requesting a multi-media file (could be an audio or video file) to be sent. The server then reads the contents of the requested multi-media file in size randomly distributed between 1000 and 2000 bytes and sends the contents read to the client as a datagram packet. The last datagram packet that will be transmitted could be of size less than 1000 bytes, if required. The client reads the bytes, datagram packets, sent from the server. As soon as a reasonable number of bytes are received at the client side, the user working at the client side should be able to launch a media player and view/hear the portions of the received multi-media file while the downloading is in progress.

### ✅ Requirements Fulfillment

| Requirement | Implementation | Location in Code |
|------------|----------------|------------------|
| **Connectionless sockets** | UDP sockets used throughout | `socket.SOCK_DGRAM` in server.py & client.py |
| **Client requests file** | Client sends START_STREAM message | `client.py` line ~216 |
| **Random packet size (1000-2000)** | `random.randint(1000, 2000)` | `server.py` line ~282 |
| **Last packet < 1000 allowed** | Reads remaining bytes naturally | `server.py` line ~283-288 |
| **Client receives datagrams** | `recvfrom()` receives UDP packets | `client.py` line ~236 |
| **Progressive playback** | Launches player at 100KB threshold | `client.py` line ~272-278 |
| **Professional interface** | Modern GUI with Tkinter | All .py files |
| **User-friendly** | Step-by-step instructions in UI | main_gui.py, server.py, client.py |

### Code Evidence

**UDP Socket Creation:**
```python
# server.py
self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

**Random Packet Sizing:**
```python
# server.py - Line 282
chunk_size = random.randint(1000, 2000)
chunk = f.read(chunk_size)
```

**Progressive Playback:**
```python
# client.py - Line 272
if (not self.playback_started and 
    bytes_received >= buffer_threshold and 
    self.auto_play_var.get()):
    self.playback_started = True
    self.launch_media_player()
```

### Project Exceeds Requirements

**Additional Features Beyond Requirements:**
- ✨ Professional GUI (not required)
- ✨ Real-time progress tracking
- ✨ Download speed calculation
- ✨ Multi-client support
- ✨ Configurable settings
- ✨ Error handling and recovery
- ✨ System check utility
- ✨ Comprehensive documentation  

## 🛠️ Troubleshooting

### Server won't start
- Ensure the port is not already in use
- Check file permissions for the selected media file
- Try using a different port number

### Client can't connect
- Verify server is running
- Check IP address and port match server configuration
- Ensure firewall allows UDP traffic on the specified port

### Media player won't launch
- Verify file format is supported by your system
- Check that default media player is configured
- Manually open the file from the downloads folder

### Download is slow
- This is normal for demonstration purposes
- Adjust `STREAMING_DELAY` in config.py to increase speed
- Check network connection if using over network

## 📝 Notes

- The application creates a `downloads` folder automatically
- Downloaded files are timestamped if duplicates exist
- UDP is connectionless, so packet loss may occur on unreliable networks
- For production use, consider adding error correction and retry mechanisms

## 🎨 Screenshots

The application features:
- Modern, professional GUI design
- Real-time progress indicators
- Detailed logging consoles
- Intuitive button layouts
- Color-coded status indicators

## 👨‍💻 Author

**Prosenjit Mondol**  
Lab Project - 5th Semester  
Date: November 21, 2025

## 📄 License

This project is created for academic purposes.

## 🙏 Acknowledgments

- Built using Python's tkinter for GUI
- Uses standard socket library for networking
- Demonstrates UDP-based streaming protocols
