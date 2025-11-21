"""
Professional UDP Streaming Client
Receives and plays multimedia files using connectionless UDP sockets
Author: Your Name
Date: November 21, 2025
"""

import socket
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from datetime import datetime
import threading
import time
import subprocess
import sys


class StreamingClientGUI:
    """Professional Streaming Client with GUI Interface"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("📥 RECEIVE Files - Client")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Client state
        self.is_downloading = False
        self.client_socket = None
        self.output_file = None
        self.playback_started = False
        self.download_thread = None
        
        # Configure style
        self.setup_styles()
        
        # Create GUI components
        self.create_widgets()
        
        # Protocol to handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Configure modern styling for widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        accent_color = "#3498db"
        success_color = "#27ae60"
        danger_color = "#e74c3c"
        warning_color = "#f39c12"
        
        style.configure("Title.TLabel", 
                       font=("Segoe UI", 16, "bold"),
                       foreground=accent_color,
                       background="white")
        
        style.configure("Info.TLabel",
                       font=("Segoe UI", 10),
                       foreground="#34495e",
                       background="white")
        
        style.configure("Success.TButton",
                       font=("Segoe UI", 10, "bold"),
                       foreground="white",
                       background=success_color)
        
        style.configure("Danger.TButton",
                       font=("Segoe UI", 10, "bold"),
                       foreground="white",
                       background=danger_color)
        
        style.configure("Primary.TButton",
                       font=("Segoe UI", 10, "bold"),
                       foreground="white",
                       background=accent_color)
        
        style.configure("Warning.TButton",
                       font=("Segoe UI", 10, "bold"),
                       foreground="white",
                       background=warning_color)
    
    def create_widgets(self):
        """Create all GUI components"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title with instructions
        title_label = ttk.Label(main_frame,
                               text="📥 Receive & Download Files",
                               style="Title.TLabel")
        title_label.pack(pady=(0, 5))
        
        instruction_label = ttk.Label(main_frame,
                                     text="Follow these 3 easy steps to download and play media:",
                                     font=("Segoe UI", 11),
                                     foreground="#7f8c8d")
        instruction_label.pack(pady=(0, 20))
        
        # Connection settings frame
        conn_frame = ttk.LabelFrame(main_frame, text="STEP 1: Enter Server Details 🔗", padding="15")
        conn_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Help text
        help_label = ttk.Label(conn_frame,
                              text="💡 Same computer? Use 'localhost' | Different computer? Ask for their IP address",
                              font=("Segoe UI", 9),
                              foreground="#f39c12")
        help_label.grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 10))
        
        # Server address
        ttk.Label(conn_frame, text="Server IP Address:", style="Info.TLabel").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.server_entry = ttk.Entry(conn_frame, width=20, font=("Segoe UI", 10))
        self.server_entry.insert(0, "localhost")
        self.server_entry.grid(row=1, column=1, sticky=tk.W, padx=(0, 30))
        
        # Port
        ttk.Label(conn_frame, text="Port (default is fine):", style="Info.TLabel").grid(row=1, column=2, sticky=tk.W, padx=(0, 10))
        self.port_entry = ttk.Entry(conn_frame, width=10, font=("Segoe UI", 10))
        self.port_entry.insert(0, "10000")
        self.port_entry.grid(row=1, column=3, sticky=tk.W)
        
        # Save location frame
        save_frame = ttk.LabelFrame(main_frame, text="STEP 2: Choose Where to Save 💾", padding="15")
        save_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.save_label = ttk.Label(save_frame,
                                    text=f"📂 {os.path.join(os.getcwd(), 'downloads')}",
                                    style="Info.TLabel",
                                    wraplength=650)
        self.save_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(save_frame,
                               text="Change Folder",
                               command=self.select_save_location,
                               style="Primary.TButton")
        browse_btn.pack(side=tk.RIGHT)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="STEP 3: Start Download & Watch Progress 📊", padding="15")
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_bar = ttk.Progressbar(progress_frame,
                                           mode='determinate',
                                           length=400)
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_label = ttk.Label(progress_frame,
                                       text="Ready to connect",
                                       style="Info.TLabel")
        self.progress_label.pack()
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.connect_btn = ttk.Button(button_frame,
                                      text="✅ START DOWNLOAD NOW",
                                      command=self.start_download,
                                      style="Success.TButton",
                                      width=25)
        self.connect_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.cancel_btn = ttk.Button(button_frame,
                                     text="⬛ STOP DOWNLOAD",
                                     command=self.cancel_download,
                                     style="Danger.TButton",
                                     width=18,
                                     state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.play_btn = ttk.Button(button_frame,
                                   text="▶️ PLAY FILE",
                                   command=self.play_media,
                                   style="Warning.TButton",
                                   width=15,
                                   state=tk.DISABLED)
        self.play_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = ttk.Button(button_frame,
                              text="🗑 Clear Log",
                              command=self.clear_log,
                              style="Primary.TButton",
                              width=12)
        clear_btn.pack(side=tk.RIGHT)
        
        # Auto-play checkbox
        self.auto_play_var = tk.BooleanVar(value=True)
        auto_play_check = ttk.Checkbutton(button_frame,
                                         text="✓ Auto-play when enough downloaded",
                                         variable=self.auto_play_var)
        auto_play_check.pack(side=tk.RIGHT, padx=(0, 20))
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="📋 Activity Log (What's happening)", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                  height=12,
                                                  font=("Consolas", 9),
                                                  bg="#1e1e1e",
                                                  fg="#d4d4d4",
                                                  insertbackground="white")
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Statistics frame
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.stats_label = ttk.Label(stats_frame,
                                     text="No active downloads",
                                     style="Info.TLabel")
        self.stats_label.pack()
        
        # Create downloads directory
        self.downloads_dir = os.path.join(os.getcwd(), 'downloads')
        os.makedirs(self.downloads_dir, exist_ok=True)
    
    def log(self, message):
        """Add timestamped message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.update()
    
    def clear_log(self):
        """Clear the log text"""
        self.log_text.delete(1.0, tk.END)
    
    def select_save_location(self):
        """Select directory to save downloaded files"""
        directory = filedialog.askdirectory(
            title="Select Download Location",
            initialdir=self.downloads_dir
        )
        
        if directory:
            self.downloads_dir = directory
            self.save_label.config(text=f"📂 {directory}")
            self.log(f"Download location changed to: {directory}")
    
    def start_download(self):
        """Initiate connection and download"""
        server_address = self.server_entry.get().strip()
        
        if not server_address:
            messagebox.showwarning("Invalid Input", "Please enter server IP address.")
            return
        
        try:
            port = int(self.port_entry.get())
            if port < 1024 or port > 65535:
                raise ValueError("Port must be between 1024 and 65535")
        except ValueError as e:
            messagebox.showerror("Invalid Port", str(e))
            return
        
        self.is_downloading = True
        self.playback_started = False
        
        # Update UI
        self.connect_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.play_btn.config(state=tk.DISABLED)
        self.server_entry.config(state=tk.DISABLED)
        self.port_entry.config(state=tk.DISABLED)
        self.progress_bar['value'] = 0
        
        self.log("="*60)
        self.log(f"Connecting to {server_address}:{port}...")
        
        # Start download in separate thread
        self.download_thread = threading.Thread(
            target=self.download_file,
            args=(server_address, port),
            daemon=True
        )
        self.download_thread.start()
    
    def download_file(self, server_address, port):
        """Main download logic"""
        try:
            # Create UDP socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.client_socket.settimeout(10.0)  # 10 second timeout
            
            # Send connection request
            message = b'START_STREAM'
            self.client_socket.sendto(message, (server_address, port))
            self.log("Connection request sent")
            
            # Receive file metadata
            data, _ = self.client_socket.recvfrom(1024)
            metadata = data.decode().split('|')
            
            if len(metadata) != 2:
                raise Exception("Invalid metadata received from server")
            
            filename, file_size_str = metadata
            file_size = int(file_size_str)
            
            self.log(f"Receiving: {filename}")
            self.log(f"File size: {file_size / (1024*1024):.2f} MB")
            
            # Prepare output file
            self.output_file = os.path.join(self.downloads_dir, filename)
            
            # If file exists, add timestamp
            if os.path.exists(self.output_file):
                name, ext = os.path.splitext(filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{name}_{timestamp}{ext}"
                self.output_file = os.path.join(self.downloads_dir, filename)
            
            self.log(f"Saving to: {self.output_file}")
            
            # Download file
            bytes_received = 0
            packet_count = 0
            start_time = time.time()
            buffer_threshold = 100 * 1024  # 100 KB to start playback
            
            with open(self.output_file, 'wb') as f:
                while self.is_downloading:
                    try:
                        data, _ = self.client_socket.recvfrom(2048)
                        
                        if data == b"EOF":
                            self.log("End of transmission received")
                            break
                        
                        # Write data
                        f.write(data)
                        bytes_received += len(data)
                        packet_count += 1
                        
                        # Update progress
                        progress = (bytes_received / file_size) * 100
                        self.progress_bar['value'] = progress
                        
                        # Calculate speed
                        elapsed = time.time() - start_time
                        if elapsed > 0:
                            speed = bytes_received / elapsed / 1024  # KB/s
                            remaining = (file_size - bytes_received) / (speed * 1024) if speed > 0 else 0
                            
                            self.progress_label.config(
                                text=f"{progress:.1f}% - {bytes_received/(1024*1024):.2f}/{file_size/(1024*1024):.2f} MB - {speed:.1f} KB/s - ETA: {remaining:.0f}s"
                            )
                            self.stats_label.config(
                                text=f"Packets received: {packet_count} | Speed: {speed:.1f} KB/s"
                            )
                        
                        # Log every 100 packets
                        if packet_count % 100 == 0:
                            self.log(f"Progress: {progress:.1f}% ({packet_count} packets)")
                        
                        # Auto-play when buffer threshold reached
                        if (not self.playback_started and 
                            bytes_received >= buffer_threshold and 
                            self.auto_play_var.get()):
                            self.playback_started = True
                            self.log(f"Buffer threshold reached ({bytes_received/(1024):.1f} KB)")
                            self.log("Launching media player...")
                            self.root.after(0, self.play_media)
                        
                    except socket.timeout:
                        self.log("Socket timeout - connection lost")
                        break
            
            # Download complete
            if bytes_received >= file_size:
                self.log(f"✓ Download completed successfully!")
                self.log(f"Total: {bytes_received} bytes in {packet_count} packets")
                self.log(f"Time: {time.time() - start_time:.1f} seconds")
                self.progress_label.config(text="Download completed!")
                self.stats_label.config(text=f"File saved: {self.output_file}")
                self.root.after(0, lambda: self.play_btn.config(state=tk.NORMAL))
                
                if not self.playback_started and self.auto_play_var.get():
                    self.root.after(0, self.play_media)
            else:
                self.log(f"⚠ Download incomplete: {bytes_received}/{file_size} bytes")
                self.progress_label.config(text="Download incomplete")
        
        except socket.timeout:
            self.log("✗ Connection timeout - server not responding")
            messagebox.showerror("Connection Error", "Server is not responding")
        
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            messagebox.showerror("Download Error", str(e))
        
        finally:
            if self.client_socket:
                self.client_socket.close()
            
            self.is_downloading = False
            self.root.after(0, self.reset_ui)
    
    def cancel_download(self):
        """Cancel ongoing download"""
        if self.is_downloading:
            self.is_downloading = False
            self.log("Download cancelled by user")
            self.progress_label.config(text="Download cancelled")
    
    def reset_ui(self):
        """Reset UI to initial state"""
        self.connect_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        self.server_entry.config(state=tk.NORMAL)
        self.port_entry.config(state=tk.NORMAL)
    
    def play_media(self):
        """Launch media player to play downloaded file"""
        if not self.output_file or not os.path.exists(self.output_file):
            messagebox.showwarning("No File", "No media file available to play")
            return
        
        try:
            self.log(f"Opening media player for: {os.path.basename(self.output_file)}")
            
            # Platform-specific media player launch
            if sys.platform.startswith('win'):
                os.startfile(self.output_file)
            elif sys.platform.startswith('darwin'):  # macOS
                subprocess.run(['open', self.output_file])
            else:  # Linux
                subprocess.run(['xdg-open', self.output_file])
            
            self.log("Media player launched successfully")
        
        except Exception as e:
            self.log(f"Error launching media player: {str(e)}")
            messagebox.showerror("Playback Error", 
                               f"Could not open media player:\n{str(e)}\n\nFile location:\n{self.output_file}")
    
    def on_closing(self):
        """Handle window close event"""
        if self.is_downloading:
            if messagebox.askokcancel("Quit", "Download in progress. Do you want to cancel and quit?"):
                self.cancel_download()
                time.sleep(0.5)
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = StreamingClientGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()