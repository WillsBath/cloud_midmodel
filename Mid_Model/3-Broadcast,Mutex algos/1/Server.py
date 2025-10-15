# ============================================================
# SERVER CODE (server_message_passing.py)
# ============================================================
# AIM:
# To implement a message passing system using sockets, where
# multiple clients can connect to a central server and exchange messages.
#
# PROCEDURE TO EXECUTE:
# 1. Save this file as "server_message_passing.py".
# 2. Open a terminal window.
# 3. Run the server using:
#       python server_message_passing.py
# 4. The server will start listening for incoming client connections.
# 5. Keep this window open — do not close it.
# 6. Then open multiple terminals and run the client program (client_message_passing.py)
#    from each one to simulate multiple clients.
# 7. Messages sent from one client will be broadcast to all others.
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

clients = []  # List to store connected client sockets

# Step 3: Broadcast message to all connected clients
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

# Step 4: Handle messages from each client
def handle_client(client_socket, address):
    print(f"New connection from {address}")
    client_socket.send("Connected to message server!\n".encode())

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Message from {address}: {message.decode().strip()}")
            broadcast(message, client_socket)
        except:
            break

    # Remove disconnected client
    clients.remove(client_socket)
    client_socket.close()
    print(f"Client {address} disconnected.")

# Step 5: Accept multiple client connections
def start_server():
    while True:
        client_socket, address = server_socket.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()

# Step 6: Run the server
start_server()
