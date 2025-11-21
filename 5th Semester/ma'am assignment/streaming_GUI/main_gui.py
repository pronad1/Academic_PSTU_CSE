import tkinter as tk
from tkinter import ttk, messagebox
import threading
from server import udp_server
from client import udp_client

def run_server():
    server_thread = threading.Thread(target=udp_server)
    server_thread.daemon = True
    server_thread.start()
    messagebox.showinfo("Server Status", "Server is running in the background.")

def run_client():
    client_thread = threading.Thread(target=udp_client)
    client_thread.daemon = True
    client_thread.start()
    messagebox.showinfo("Client Status", "Client is running in the background.")

# Create the main window
root = tk.Tk()
root.title("Streaming Application")
root.geometry("400x250")
root.configure(bg="#f0f0f0")

# Style for the widgets
style = ttk.Style()
style.configure("TButton",
                font=("Helvetica", 12, "bold"),
                padding=10,
                borderwidth=2,
                relief="raised",
                background="#4CAF50",
                foreground="white")
style.map("TButton",
          background=[('active', '#45a049')])

# Main frame
main_frame = ttk.Frame(root, padding=20, style="TFrame")
main_frame.pack(expand=True, fill="both")
style.configure("TFrame", background="#f0f0f0")

# Title label
title_label = ttk.Label(main_frame,
                        text="Select an option",
                        font=("Helvetica", 16, "bold"),
                        background="#f0f0f0")
title_label.pack(pady=10)

# Button frame
button_frame = ttk.Frame(main_frame, style="TFrame")
button_frame.pack(pady=20)

# Create and place the buttons
server_button = ttk.Button(button_frame, text="Run Server", command=run_server, style="TButton")
server_button.pack(side="left", padx=10)

client_button = ttk.Button(button_frame, text="Run Client", command=run_client, style="TButton")
client_button.pack(side="right", padx=10)

# Start the GUI event loop
root.mainloop()