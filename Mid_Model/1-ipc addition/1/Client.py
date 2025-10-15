# ============================================================
# CLIENT CODE (client.py)
# ============================================================
# PROCEDURE TO EXECUTE:
# 1. Save this file as "client.py".
# 2. Make sure the server (server.py) is already running.
# 3. Open a new terminal or command prompt.
# 4. Run this command:  python client.py
# 5. Enter numbers separated by spaces when prompted (e.g., 10 20 30).
# 6. The client will send them to the server and print the sum.
# ============================================================

import socket

# Step 1: Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Step 2: Connect to the server
HOST = 'localhost'
PORT = 12345
client_socket.connect((HOST, PORT))

# Step 3: Send message to the server
message = input("Enter numbers separated by spaces: ")  # Example: 10 20 30
client_socket.send(message.encode())

# Step 4: Receive and print response from server
response = client_socket.recv(1024).decode()
print(f"Server response: {response}")

# Step 5: Close connection
client_socket.close()
