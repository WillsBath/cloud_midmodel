# ============================================================
# SERVER CODE (server_message_passing.py)
# ============================================================
# AIM:
# To implement a message passing system where multiple clients
# can connect and send messages either to all clients (broadcast)
# or to one specific client by addressing them with @name.
#
# FORMAT TO SEND PRIVATE MESSAGE:
#       @receiver_name message
#
# Example:
#       @john Hello!
# ============================================================

import socket
import threading

# Step 1: Server setup — host and port
HOST = 'localhost'
PORT = 5000

# Step 2: Create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server started. Listening on {HOST}:{PORT}...")

clients = {}   # Store {client_name: client_socket}

# Step 3: Send message to one particular client
def send_private(receiver, message):
    if receiver in clients:
        try:
            clients[receiver].send(message.encode())
        except:
            del clients[receiver]
    else:
        print(f"User '{receiver}' not found.")

# Step 4: Broadcast message to all clients except the sender
def broadcast(message, sender_socket):
    for client_name, sock in clients.items():
        if sock != sender_socket:
            try:
                sock.send(message.encode())
            except:
                del clients[client_name]

# Step 5: Handle each client separately
def handle_client(client_socket, address):
    # First receive the client name right after connection
    client_name = client_socket.recv(1024).decode().strip()
    clients[client_name] = client_socket

    print(f"New client '{client_name}' connected from {address}")
    client_socket.send("Connected to server!\n".encode())

    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            print(f"Message from {client_name}: {data}")

            # Check if message is a private message
            if data.startswith("@"):
                parts = data.split(" ", 1)
                receiver = parts[0][1:]           # remove @
                message_body = parts[1] if len(parts) > 1 else ""

                full_msg = f"[PRIVATE from {client_name}] {message_body}"
                send_private(receiver, full_msg)

            else:
                # Normal message → broadcast
                full_msg = f"{client_name}: {data}"
                broadcast(full_msg, client_socket)

        except:
            break

    # On disconnect
    del clients[client_name]
    client_socket.close()
    print(f"Client '{client_name}' disconnected.")

# Step 6: Accept incoming connections
def start_server():
    while True:
        client_socket, address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()

# Step 7: Run server
start_server()
