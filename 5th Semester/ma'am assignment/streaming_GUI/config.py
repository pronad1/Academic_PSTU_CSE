"""
Configuration file for UDP Streaming Application
Contains default settings and constants
Author: Your Name
Date: November 21, 2025
"""

# Network Configuration
DEFAULT_SERVER_IP = "localhost"
DEFAULT_PORT = 10000
SOCKET_TIMEOUT = 10.0  # seconds

# Packet Configuration
MIN_PACKET_SIZE = 1000  # bytes
MAX_PACKET_SIZE = 2000  # bytes
RECEIVE_BUFFER_SIZE = 2048  # bytes

# Client Configuration
PLAYBACK_THRESHOLD = 100 * 1024  # 100 KB - minimum data to start playback
AUTO_PLAY_ENABLED = True
DOWNLOAD_FOLDER = "downloads"

# Server Configuration
STREAMING_DELAY = 0.01  # seconds between packets
MAX_CONNECTIONS = 10  # maximum concurrent connections

# File Types
SUPPORTED_VIDEO_FORMATS = [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"]
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"]

# UI Configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
LOG_UPDATE_INTERVAL = 100  # packets between log updates

# Colors (for GUI theming)
COLORS = {
    "primary": "#3498db",
    "success": "#27ae60",
    "danger": "#e74c3c",
    "warning": "#f39c12",
    "info": "#34495e",
    "dark": "#2c3e50",
    "light": "#ecf0f1"
}

# Application Information
APP_NAME = "UDP Media Streaming"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Name"
APP_DESCRIPTION = "Professional connectionless socket-based media streaming application"
