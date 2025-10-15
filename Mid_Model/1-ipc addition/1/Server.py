# ============================================================
# SERVER CODE (server.py)
# ============================================================
# PROCEDURE TO EXECUTE:
# 1. Save this file as "server.py".
# 2. Open a terminal or command prompt.
# 3. Run this command first:  python server.py
# 4. The server will start listening for client connections.
# 5. Keep this window open — do not close it.
# 6. Now open another terminal and run the client code (client.py).
# ============================================================

import socket

# Step 1: Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Step 2: Bind the socket to host and port
HOST = 'localhost'   # or use '127.0.0.1'
PORT = 12345
server_socket.bind((HOST, PORT))

# Step 3: Listen for client connections
server_socket.listen(1)
print(f"Server is listening on {HOST}:{PORT}...")

# Step 4: Accept client connection
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# Step 5: Receive data from client
data = conn.recv(1024).decode()
print(f"Received from client: {data}")

# Step 6: Parse numbers and compute sum
try:
    numbers = list(map(int, data.split()))
    result = sum(numbers)
    response = f"Sum = {result}"
except ValueError:
    response = "Please send valid integers separated by spaces."

# Step 7: Send response back to client
conn.send(response.encode())

# Step 8: Close the connection
conn.close()
server_socket.close()
print("Server closed connection.")
