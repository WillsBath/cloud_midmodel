# ============================================================
# CLIENT CODE (client_message_passing.py)
# ============================================================
# AIM:
# To connect to the message-passing server and send messages
# either to all clients or a specific client using @name syntax.
#
# PRIVATE MESSAGE FORMAT:
#       @receiver_name message text
#
# Example:
#       @john Hello bro!

# Steps to execute
# 1. run "python server_message_passing.py" in one terminal
# 2. run "python client_message_passing.py" in other terminals
# 3. give a unique name for each client
# 4. to broadcast the message , just give the message you need to broadcast.
# 5. for private message follow "@receiver_name message" format.
# 6. to exit the chat "type exit"

# ============================================================

import socket
import threading

HOST = 'localhost'
PORT = 5000

# Create client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Step 1: Send name immediately after connecting
name = input("Enter your name: ")
client_socket.send(name.encode())

print("Connected! You can start chatting...")
print("Use: @username message  → to send private message\n")

# Thread to receive messages
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

# Thread to send messages
def send_messages():
    while True:
        message = input("")
        if message.lower() == "exit":
            client_socket.close()
            break

        # Message is sent exactly as typed
        client_socket.send(message.encode())

# Start threads
threading.Thread(target=receive_messages, daemon=True).start()
send_messages()
