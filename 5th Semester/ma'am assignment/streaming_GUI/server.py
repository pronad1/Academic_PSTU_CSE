"""
Professional UDP Streaming Server
Supports streaming of multimedia files using connectionless UDP sockets
Author: Your Name
Date: November 21, 2025
"""

import socket
import os
import random
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
import threading


class StreamingServerGUI:
    """Professional Streaming Server with GUI Interface"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("📤 SHARE Files - Server")
        self.root.geometry("850x650")
        self.root.minsize(750, 550)
        
        # Server state
        self.is_running = False
        self.server_socket = None
        self.selected_file = None
        self.port = 10000
        
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
        bg_color = "#2c3e50"
        fg_color = "#ecf0f1"
        accent_color = "#3498db"
        success_color = "#27ae60"
        danger_color = "#e74c3c"
        
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
    
    def create_widgets(self):
        """Create all GUI components"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title with instructions
        title_label = ttk.Label(main_frame,
                               text="📤 Share Your Files",
                               style="Title.TLabel")
        title_label.pack(pady=(0, 5))
        
        instruction_label = ttk.Label(main_frame,
                                     text="Follow these 3 easy steps to share your media file:",
                                     font=("Segoe UI", 11),
                                     foreground="#7f8c8d")
        instruction_label.pack(pady=(0, 20))
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="STEP 1: Choose Your File 📁", padding="15")
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.file_label = ttk.Label(file_frame,
                                    text="👉 Click the button to select a video or audio file to share",
                                    style="Info.TLabel",
                                    wraplength=600)
        self.file_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(file_frame,
                               text="📂 SELECT FILE",
                               command=self.browse_file,
                               style="Primary.TButton")
        browse_btn.pack(side=tk.RIGHT)
        
        # Server configuration frame
        config_frame = ttk.LabelFrame(main_frame, text="STEP 2: Start Sharing ▶️", padding="15")
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(config_frame, text="Port (leave as default):", style="Info.TLabel").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.port_entry = ttk.Entry(config_frame, width=10)
        self.port_entry.insert(0, "10000")
        self.port_entry.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(config_frame, text="Server Status:", style="Info.TLabel").grid(row=0, column=2, sticky=tk.W, padx=(30, 10))
        self.status_label = ttk.Label(config_frame, text="⚫  Not Running", foreground="#e74c3c", font=("Segoe UI", 10, "bold"))
        self.status_label.grid(row=0, column=3, sticky=tk.W)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.start_btn = ttk.Button(button_frame,
                                    text="✅ START SHARING NOW",
                                    command=self.start_server,
                                    style="Success.TButton",
                                    width=25)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(button_frame,
                                   text="⬛ STOP SHARING",
                                   command=self.stop_server,
                                   style="Danger.TButton",
                                   width=20,
                                   state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT)
        
        clear_btn = ttk.Button(button_frame,
                              text="🗑 Clear Log",
                              command=self.clear_log,
                              style="Primary.TButton",
                              width=15)
        clear_btn.pack(side=tk.RIGHT)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="STEP 3: Monitor Activity 📊 (What's happening)", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                  height=15,
                                                  font=("Consolas", 9),
                                                  bg="#1e1e1e",
                                                  fg="#d4d4d4",
                                                  insertbackground="white")
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Statistics frame
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.stats_label = ttk.Label(stats_frame,
                                     text="Ready to serve",
                                     style="Info.TLabel")
        self.stats_label.pack()
    
    def browse_file(self):
        """Open file dialog to select media file"""
        filetypes = (
            ("Video files", "*.mp4 *.avi *.mkv *.mov *.wmv"),
            ("Audio files", "*.mp3 *.wav *.flac *.aac"),
            ("All files", "*.*")
        )
        
        filename = filedialog.askopenfilename(
            title="Select Media File",
            filetypes=filetypes
        )
        
        if filename:
            self.selected_file = filename
            file_size = os.path.getsize(filename)
            size_mb = file_size / (1024 * 1024)
            display_name = os.path.basename(filename)
            
            self.file_label.config(text=f"📁 {display_name} ({size_mb:.2f} MB)")
            self.log(f"File selected: {filename} ({size_mb:.2f} MB)")
    
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
    
    def start_server(self):
        """Start the UDP streaming server"""
        if not self.selected_file:
            messagebox.showwarning("No File Selected", 
                                  "Please select a media file to stream.")
            return
        
        if not os.path.exists(self.selected_file):
            messagebox.showerror("File Not Found",
                               "The selected file no longer exists.")
            return
        
        try:
            self.port = int(self.port_entry.get())
            if self.port < 1024 or self.port > 65535:
                raise ValueError("Port must be between 1024 and 65535")
        except ValueError as e:
            messagebox.showerror("Invalid Port", str(e))
            return
        
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="🟢  Sharing Active", foreground="#27ae60")
        self.port_entry.config(state=tk.DISABLED)
        
        self.log("="*60)
        self.log("Server starting...")
        
        # Start server in separate thread
        server_thread = threading.Thread(target=self.run_server, daemon=True)
        server_thread.start()
    
    def run_server(self):
        """Main server loop"""
        try:
            # Create UDP socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.settimeout(1.0)  # Set timeout for graceful shutdown
            
            server_address = ('0.0.0.0', self.port)
            self.server_socket.bind(server_address)
            
            self.log(f"Server bound to {server_address}")
            self.log("Waiting for client requests...")
            
            while self.is_running:
                try:
                    # Wait for client request
                    data, client_address = self.server_socket.recvfrom(1024)
                    self.log(f"Connection from {client_address}")
                    
                    # Handle client request in separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_address,),
                        daemon=True
                    )
                    client_thread.start()
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.is_running:
                        self.log(f"Error: {str(e)}")
        
        except Exception as e:
            self.log(f"Server error: {str(e)}")
            messagebox.showerror("Server Error", str(e))
        
        finally:
            if self.server_socket:
                self.server_socket.close()
            self.log("Server stopped")
    
    def handle_client(self, client_address):
        """Handle individual client streaming request"""
        try:
            file_size = os.path.getsize(self.selected_file)
            
            # Send file metadata
            filename = os.path.basename(self.selected_file)
            metadata = f"{filename}|{file_size}".encode()
            self.server_socket.sendto(metadata, client_address)
            self.log(f"Sent metadata to {client_address}: {filename} ({file_size} bytes)")
            
            # Small delay to ensure client is ready
            time.sleep(0.1)
            
            # Stream file
            bytes_sent = 0
            packet_count = 0
            
            with open(self.selected_file, 'rb') as f:
                while self.is_running:
                    # Random chunk size between 1000 and 2000 bytes
                    chunk_size = random.randint(1000, 2000)
                    chunk = f.read(chunk_size)
                    
                    if not chunk:
                        # End of file
                        self.server_socket.sendto(b"EOF", client_address)
                        self.log(f"EOF sent to {client_address}")
                        break
                    
                    # Send chunk
                    self.server_socket.sendto(chunk, client_address)
                    bytes_sent += len(chunk)
                    packet_count += 1
                    
                    # Log progress every 50 packets
                    if packet_count % 50 == 0:
                        progress = (bytes_sent / file_size) * 100
                        self.log(f"Progress: {progress:.1f}% ({bytes_sent}/{file_size} bytes)")
                        self.stats_label.config(
                            text=f"Streaming to {client_address[0]}:{client_address[1]} - {progress:.1f}% complete"
                        )
                    
                    # Simulate streaming delay
                    time.sleep(0.01)
            
            self.log(f"Completed: Sent {bytes_sent} bytes in {packet_count} packets to {client_address}")
            self.stats_label.config(text="Stream completed - Ready for next client")
            
        except Exception as e:
            self.log(f"Error handling client {client_address}: {str(e)}")
    
    def stop_server(self):
        """Stop the UDP streaming server"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="⚫  Not Running", foreground="#e74c3c")
        self.port_entry.config(state=tk.NORMAL)
        self.stats_label.config(text="Ready to share files")
        self.log("Server shutdown initiated...")
    
    def on_closing(self):
        """Handle window close event"""
        if self.is_running:
            if messagebox.askokcancel("Quit", "Server is running. Do you want to stop it and quit?"):
                self.stop_server()
                time.sleep(0.5)
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = StreamingServerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()