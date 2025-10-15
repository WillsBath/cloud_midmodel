# ============================================================
# SERVER CODE (server_object.py)
# ============================================================
# PROCEDURE TO EXECUTE:
# 1. Save this file as "server_object.py".
# 2. Open a terminal or command prompt.
# 3. Run this command first:  python server_object.py
# 4. The server will start listening for client connections.
# 5. Keep this terminal open — do not close it.
# 6. Then open another terminal window and run the client code (client_object.py).
# 7. The server will receive a serialized object, compute the sum, and respond.
# ============================================================

import socket
import pickle

# Step 1: Define the same DataObject class used by the client
class DataObject:
    def __init__(self, name, values):
        self.name = name
        self.values = values

# Step 2: Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Step 3: Bind to host and port
HOST = 'localhost'
PORT = 12346
server_socket.bind((HOST, PORT))

# Step 4: Listen for incoming connections
server_socket.listen(1)
print(f"Server is listening on {HOST}:{PORT}...")

# Step 5: Accept client connection
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# Step 6: Receive serialized data from client
data = conn.recv(4096)
data_object = pickle.loads(data)  # Deserialize the object

print(f"Received object from client:")
print(f"Name: {data_object.name}")
print(f"Values: {data_object.values}")

# Step 7: Compute sum of values
try:
    total = sum(data_object.values)
    response = f"Hello {data_object.name}, Sum of your values is {total}."
except Exception as e:
    response = f"Error while computing sum: {e}"

# Step 8: Send the response back to the client
conn.send(response.encode())

# Step 9: Close connection
conn.close()
server_socket.close()
print("Server closed connection.")
