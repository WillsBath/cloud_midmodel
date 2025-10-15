# ============================================================
# Ricart–Agrawala Distributed Mutual Exclusion
# ============================================================
# AIM:
# To implement the Ricart–Agrawala algorithm using sockets.
#
# PROCEDURE TO EXECUTE:
# 1. Save this file as "ricart_agrawala.py".
# 2. Open multiple terminals (say 3).
# 3. Run each process with a different port number:
#       python ricart_agrawala.py 5001
#       python ricart_agrawala.py 5002
#       python ricart_agrawala.py 5003
# 4. When prompted, type 'request' in one terminal to request
#    access to the Critical Section.
# 5. Observe message passing between processes.
# 6. Type Ctrl+C to stop any process.
# ============================================================

import socket
import threading
import sys
import time

PORTS = [5001, 5002, 5003]  # List of process ports
HOST = 'localhost'

my_port = int(sys.argv[1])
timestamp = 0
replies = 0
requesting = False

def listener():
    """Listen for messages from other processes."""
    global replies, requesting, timestamp
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, my_port))
    print(f"[Process {my_port}] Listening...")
    while True:
        data, addr = s.recvfrom(1024)
        msg = data.decode().split()
        if msg[0] == 'REQUEST':
            req_time = int(msg[1])
            sender = int(msg[2])
            # Reply if not requesting or has smaller timestamp
            if not requesting or (req_time > timestamp or (req_time == timestamp and sender > my_port)):
                reply(sender)
        elif msg[0] == 'REPLY':
            replies += 1

def reply(dest_port):
    """Send REPLY message to requester."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(f"REPLY {my_port}".encode(), (HOST, dest_port))

def request_CS():
    """Request entry to critical section."""
    global timestamp, requesting, replies
    requesting = True
    timestamp = int(time.time())
    replies = 0
    print(f"[{my_port}] Requesting CS at time {timestamp}")
    for port in PORTS:
        if port != my_port:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(f"REQUEST {timestamp} {my_port}".encode(), (HOST, port))
    while replies < len(PORTS) - 1:
        time.sleep(0.5)
    print(f"[{my_port}] Entered Critical Section!")
    time.sleep(3)
    print(f"[{my_port}] Exiting Critical Section.")
    requesting = False
    replies = 0

# Start listener thread
threading.Thread(target=listener, daemon=True).start()

# Simple console interface
while True:
    cmd = input("Type 'request' to enter CS: ")
    if cmd.lower() == 'request':
        request_CS()
