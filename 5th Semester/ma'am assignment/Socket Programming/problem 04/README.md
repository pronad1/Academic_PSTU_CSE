# Streaming Server using UDP

## Files:
- `server.py` - UDP streaming server
- `client.py` - Streaming client with buffering

## How to Run:

1. Place a multimedia file (audio/video) in server directory
2. Start server: `python server.py`
3. Run client: `python client.py`
4. Enter filename (e.g., `video.mp4` or `audio.mp3`)
5. After 10KB buffered, launch media player to play while downloading

## Features:
- UDP connectionless streaming
- Random chunk size (1000-2000 bytes)
- Client buffers before playback
- Can play while downloading continues

## Example:
After buffering, open with media player:
- `vlc streaming_video.mp4`
- `ffplay streaming_audio.mp3`
