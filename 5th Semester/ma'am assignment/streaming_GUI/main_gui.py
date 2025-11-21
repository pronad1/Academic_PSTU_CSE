"""
Professional UDP Streaming Application Launcher
Main interface to launch server or client applications
Author: Your Name
Date: November 21, 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os


class StreamingLauncherGUI:
    """Professional launcher for streaming server and client"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Media Streaming - Easy File Sharing")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        
        # Configure styling
        self.setup_styles()
        
        # Create GUI
        self.create_widgets()
        
        # Center window
        self.center_window()
    
    def setup_styles(self):
        """Configure modern styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colors
        primary_color = "#3498db"
        success_color = "#27ae60"
        info_color = "#34495e"
        
        style.configure("Title.TLabel",
                       font=("Segoe UI", 24, "bold"),
                       foreground=primary_color,
                       background="white")
        
        style.configure("Subtitle.TLabel",
                       font=("Segoe UI", 11),
                       foreground=info_color,
                       background="white")
        
        style.configure("Header.TLabel",
                       font=("Segoe UI", 14, "bold"),
                       foreground=primary_color,
                       background="white")
        
        style.configure("Info.TLabel",
                       font=("Segoe UI", 10),
                       foreground="#7f8c8d",
                       background="white")
        
        style.configure("Feature.TLabel",
                       font=("Segoe UI", 9),
                       foreground="#2c3e50",
                       background="white")
    
    def create_widgets(self):
        """Create all GUI components"""
        # Main container with gradient background
        self.root.configure(bg="#ecf0f1")
        
        # Header with colored background
        header_frame = tk.Frame(self.root, bg="#3498db", height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Title with icon
        title_label = tk.Label(header_frame,
                              text="🎬 Media Streaming App",
                              font=("Segoe UI", 28, "bold"),
                              bg="#3498db",
                              fg="white")
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(header_frame,
                                 text="Easy File Sharing Over Network",
                                 font=("Segoe UI", 12),
                                 bg="#3498db",
                                 fg="#ecf0f1")
        subtitle_label.pack()
        
        # Main content area
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Instructions
        instruction_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        instruction_frame.pack(fill=tk.X, pady=(0, 20))
        
        inst_label = tk.Label(instruction_frame,
                             text="👇 Choose Your Role:",
                             font=("Segoe UI", 16, "bold"),
                             bg="white",
                             fg="#2c3e50")
        inst_label.pack(pady=15)
        
        help_text = tk.Label(instruction_frame,
                            text="Want to SHARE a file? → Click 'I Want to SHARE'\n"
                                 "Want to RECEIVE a file? → Click 'I Want to RECEIVE'",
                            font=("Segoe UI", 11),
                            bg="white",
                            fg="#7f8c8d",
                            justify=tk.CENTER)
        help_text.pack(pady=(0, 15))
        
        # Buttons container
        buttons_frame = tk.Frame(main_frame, bg="#ecf0f1")
        buttons_frame.pack(expand=True)
        
        # Server button (simplified)
        server_container = tk.Frame(buttons_frame, bg="white", relief=tk.RAISED, bd=3)
        server_container.pack(side=tk.LEFT, padx=15)
        
        tk.Label(server_container,
                text="📤",
                font=("Segoe UI", 48),
                bg="white").pack(pady=(20, 10))
        
        tk.Label(server_container,
                text="I Want to SHARE",
                font=("Segoe UI", 16, "bold"),
                bg="white",
                fg="#27ae60").pack()
        
        tk.Label(server_container,
                text="Share your video or audio file\nwith others on the network",
                font=("Segoe UI", 10),
                bg="white",
                fg="#7f8c8d",
                justify=tk.CENTER).pack(pady=10)
        
        server_btn = tk.Button(server_container,
                              text="START SHARING",
                              command=self.launch_server,
                              font=("Segoe UI", 13, "bold"),
                              bg="#27ae60",
                              fg="white",
                              activebackground="#229954",
                              activeforeground="white",
                              cursor="hand2",
                              relief=tk.FLAT,
                              padx=40,
                              pady=15,
                              borderwidth=0)
        server_btn.pack(pady=(10, 20), padx=30)
        
        # Client button (simplified)
        client_container = tk.Frame(buttons_frame, bg="white", relief=tk.RAISED, bd=3)
        client_container.pack(side=tk.LEFT, padx=15)
        
        tk.Label(client_container,
                text="📥",
                font=("Segoe UI", 48),
                bg="white").pack(pady=(20, 10))
        
        tk.Label(client_container,
                text="I Want to RECEIVE",
                font=("Segoe UI", 16, "bold"),
                bg="white",
                fg="#3498db").pack()
        
        tk.Label(client_container,
                text="Download and watch/listen to\nfiles from another computer",
                font=("Segoe UI", 10),
                bg="white",
                fg="#7f8c8d",
                justify=tk.CENTER).pack(pady=10)
        
        client_btn = tk.Button(client_container,
                              text="START RECEIVING",
                              command=self.launch_client,
                              font=("Segoe UI", 13, "bold"),
                              bg="#3498db",
                              fg="white",
                              activebackground="#2980b9",
                              activeforeground="white",
                              cursor="hand2",
                              relief=tk.FLAT,
                              padx=40,
                              pady=15,
                              borderwidth=0)
        client_btn.pack(pady=(10, 20), padx=30)
        
        # Help section
        help_frame = tk.Frame(main_frame, bg="#fff3cd", relief=tk.RAISED, bd=2)
        help_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Label(help_frame,
                text="💡 Quick Tip:",
                font=("Segoe UI", 12, "bold"),
                bg="#fff3cd",
                fg="#856404").pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        tk.Label(help_frame,
                text="• If you're on the SAME computer, use both windows\n"
                     "• If you're on DIFFERENT computers, one person clicks SHARE, other clicks RECEIVE",
                font=("Segoe UI", 10),
                bg="#fff3cd",
                fg="#856404",
                justify=tk.LEFT).pack(anchor=tk.W, padx=15, pady=(0, 10))
    
    def create_card_frame(self, parent, title):
        """Create a styled card frame"""
        # Outer frame for shadow effect
        outer_frame = tk.Frame(parent, bg="#d5dbdb", bd=0)
        outer_frame.pack(fill=tk.X, padx=2, pady=2)
        
        # Inner frame (actual card)
        card_frame = tk.Frame(outer_frame, bg="white", relief=tk.RAISED, bd=1)
        card_frame.pack(fill=tk.BOTH, padx=1, pady=1)
        
        # Content frame with padding
        content_frame = tk.Frame(card_frame, bg="white")
        content_frame.pack(fill=tk.BOTH, padx=20, pady=15)
        
        # Title
        title_label = ttk.Label(content_frame,
                               text=title,
                               style="Header.TLabel")
        title_label.pack(anchor=tk.W, pady=(0, 10))
        
        return content_frame
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def launch_server(self):
        """Launch the server application"""
        try:
            script_path = os.path.join(os.path.dirname(__file__), 'server.py')
            
            if not os.path.exists(script_path):
                messagebox.showerror("Error", "server.py not found!")
                return
            
            # Launch in new process
            if sys.platform.startswith('win'):
                subprocess.Popen([sys.executable, script_path],
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen([sys.executable, script_path])
            
            messagebox.showinfo("✅ Sharing Window Opened!",
                              "A new window has opened where you can:\n\n"
                              "1️⃣ Click 'Browse File' to select your video/audio\n"
                              "2️⃣ Click 'Start Server' button\n"
                              "3️⃣ Wait for someone to connect!\n\n"
                              "👉 The other person needs your IP address to connect.")
        
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch server:\n{str(e)}")
    
    def launch_client(self):
        """Launch the client application"""
        try:
            script_path = os.path.join(os.path.dirname(__file__), 'client.py')
            
            if not os.path.exists(script_path):
                messagebox.showerror("Error", "client.py not found!")
                return
            
            # Launch in new process
            if sys.platform.startswith('win'):
                subprocess.Popen([sys.executable, script_path],
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen([sys.executable, script_path])
            
            messagebox.showinfo("✅ Receiving Window Opened!",
                              "A new window has opened where you can:\n\n"
                              "1️⃣ Enter the sender's IP address (or use 'localhost' if same computer)\n"
                              "2️⃣ Click 'Connect & Download'\n"
                              "3️⃣ Watch the file download and play automatically!\n\n"
                              "👉 Ask the sender for their IP address.")
        
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch client:\n{str(e)}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = StreamingLauncherGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()