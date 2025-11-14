import wave
import struct
import math

# Generate a simple 5-second audio file
sample_rate = 44100
duration = 5
frequency = 440  # A4 note

with wave.open('audio.wav', 'w') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    
    for i in range(sample_rate * duration):
        value = int(32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
        data = struct.pack('<h', value)
        wav_file.writeframes(data)

print("audio.wav created (5 seconds, 440Hz tone)")

# Generate a simple video file data (dummy data for testing)
with open('video.mp4', 'wb') as f:
    # Write minimal MP4 header structure for testing
    # This creates a small valid-looking file for transfer testing
    data = b'\x00' * 50000  # 50KB of data for testing
    f.write(data)

print("video.mp4 created (50KB test file)")
