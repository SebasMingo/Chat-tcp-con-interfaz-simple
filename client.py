import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Configuración de la conexión
host = '127.0.0.1'
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server():
    try:
        client.connect((host, port))
    except ConnectionRefusedError:
        print("Connection refused, please make sure the server is running.")
        exit()

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                add_message(message)
        except:
            print("An error occurred. Disconnecting...")
            client.close()
            break

def send_message():
    message = message_entry.get()
    add_message(f"You: {message}")
    client.send(f"{username}: {message}".encode('utf-8'))
    message_entry.delete(0, tk.END)

def add_message(message):
    message_area.config(state=tk.NORMAL)
    message_area.insert(tk.END, message + '\n')
    message_area.yview(tk.END)
    message_area.config(state=tk.DISABLED)

def on_closing():
    client.close()
    root.destroy()

def start_chat():
    global username
    username = username_entry.get()
    if username:
        login_window.destroy()
        connect_to_server()

        # Configuración de la interfaz gráfica
        global root, message_area, message_entry
        root = tk.Tk()
        root.title("Chat Client")

        frame = tk.Frame(root)
        scrollbar = tk.Scrollbar(frame)
        message_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state=tk.DISABLED, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        message_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frame.pack(fill=tk.BOTH, expand=True)

        message_entry = tk.Entry(root, width=50)
        message_entry.pack(fill=tk.X, padx=10, pady=5)
        message_entry.bind("<Return>", lambda event: send_message())

        send_button = tk.Button(root, text="Send", command=send_message)
        send_button.pack(pady=5)

        root.protocol("WM_DELETE_WINDOW", on_closing)

        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.start()

        root.mainloop()

# Ventana de inicio para ingresar el nombre de usuario
login_window = tk.Tk()
login_window.title("Login")

login_frame = tk.Frame(login_window)
login_frame.pack(pady=10)

username_label = tk.Label(login_frame, text="Enter your username:")
username_label.pack(pady=5)

username_entry = tk.Entry(login_frame)
username_entry.pack(pady=5)

login_button = tk.Button(login_frame, text="Start Chat", command=start_chat)
login_button.pack(pady=10)

login_window.mainloop()
