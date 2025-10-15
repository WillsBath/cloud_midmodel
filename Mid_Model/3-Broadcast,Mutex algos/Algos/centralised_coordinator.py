# ============================================================
# Centralized Coordinator Mutual Exclusion
# ============================================================
# AIM:
# To implement a centralized coordinator for mutual exclusion.
#
# PROCEDURE TO EXECUTE:
# 1. Save as "centralized_coordinator.py".
# 2. Open 3 terminals:
#       python centralized_coordinator.py coordinator
#       python centralized_coordinator.py process 5001
#       python centralized_coordinator.py process 5002
# 3. The coordinator grants permission one at a time.
# 4. Type 'request' in a process terminal to access CS.
# ============================================================

import socket
import threading
import sys
import time

HOST = 'localhost'
PORT = 6000
queue = []
in_cs = False

def coordinator():
    """Coordinator to grant permission to one process at a time."""
    global in_cs
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    print("[Coordinator] Waiting for requests...")
    while True:
        data, addr = s.recvfrom(1024)
        msg = data.decode()
        if msg.startswith('REQUEST'):
            pid = msg.split()[1]
            print(f"Received REQUEST from {pid}")
            if not in_cs:
                in_cs = True
                s.sendto('GRANT'.encode(), addr)
            else:
                queue.append((pid, addr))
        elif msg == 'RELEASE':
            in_cs = False
            if queue:
                pid, addr = queue.pop(0)
                s.sendto('GRANT'.encode(), addr)
                in_cs = True

def process(my_port):
    """Client process that requests CS permission."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, my_port))
    print(f"[Process {my_port}] Ready.")
    def listen():
        while True:
            data, addr = s.recvfrom(1024)
            msg = data.decode()
            if msg == 'GRANT':
                print(f"[{my_port}] Got permission — entering CS...")
                time.sleep(3)
                print(f"[{my_port}] Exiting CS and sending RELEASE.")
                send('RELEASE')
    threading.Thread(target=listen, daemon=True).start()

    def send(msg):
        c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c.sendto(msg.encode(), (HOST, PORT))

    while True:
        cmd = input("Type 'request' to enter CS: ")
        if cmd.lower() == 'request':
            send(f"REQUEST {my_port}")

# Entry point
if sys.argv[1] == 'coordinator':
    coordinator()
else:
    process(int(sys.argv[2]))
