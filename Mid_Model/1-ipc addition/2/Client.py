# ============================================================
# CLIENT CODE (client_object.py)
# ============================================================
# PROCEDURE TO EXECUTE:
# 1. Save this file as "client_object.py".
# 2. Make sure the server (server_object.py) is already running.
# 3. Open a new terminal window.
# 4. Run this command:  python client_object.py
# 5. Enter your name and a few numbers separated by spaces.
# 6. The client will send a serialized DataObject to the server.
# 7. The client will then print the response received from the server.
# ============================================================

import socket
import pickle

# Step 1: Define the same DataObject class used by the server
class DataObject:
    def __init__(self, name, values):
        self.name = name
        self.values = values

# Step 2: Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Step 3: Connect to the server
HOST = 'localhost'
PORT = 12346
client_socket.connect((HOST, PORT))

# Step 4: Get input from user
name = input("Enter your name: ")
numbers = input("Enter numbers separated by spaces: ")
values = list(map(int, numbers.split()))

# Step 5: Create DataObject and serialize it using pickle
data_object = DataObject(name, values)
serialized_data = pickle.dumps(data_object)

# Step 6: Send serialized data to the server
client_socket.send(serialized_data)

# Step 7: Receive and print server’s response
response = client_socket.recv(1024).decode()
print(f"Server response: {response}")

# Step 8: Close connection
client_socket.close()
