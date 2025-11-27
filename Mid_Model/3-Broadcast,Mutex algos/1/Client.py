# ============================================================
# CLIENT CODE (client_message_passing.py)
# ============================================================
# AIM:
# To connect to a message-passing server and exchange messages
# with other clients in a distributed system using sockets.
#
# PROCEDURE TO EXECUTE:
# 1. Save this file as "client_message_passing.py".
# 2. Ensure the server (server_message_passing.py) is already running.
# 3. Open a new terminal and run:
#       python client_message_passing.py
# 4. Enter your name when prompted.
# 5. Type messages and press ENTER to send them.
# 6. Open multiple clients in separate terminals to test message broadcasting.
# 7. Type exit to terminate
# ============================================================

import socket
import threading

# Step 1: Client setup — connect to server
HOST = 'localhost'
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Step 2: Receive messages from server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print("\n" + message)
        except:
            print("Disconnected from server.")
            client_socket.close()
            break

# Step 3: Send messages to server
def send_messages():
    name = input("Enter your name: ")
    print("You can start sending messages...")
    while True:
        message = input()
        if message.lower() == 'exit':
            client_socket.close()
            break
        full_message = f"{name}: {message}"
        client_socket.send(full_message.encode())

# Step 4: Start threads for sending and receiving
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
