# ============================================================
# Token Ring Mutual Exclusion
# ============================================================
# AIM:
# To implement Token Ring algorithm for distributed mutual exclusion.
#
# PROCEDURE TO EXECUTE:
# 1. Save as "token_ring.py".
# 2. Open 3 terminals (or more).
# 3. Run each process with different port:
#       python token_ring.py 5001 5002
#       python token_ring.py 5002 5003
#       python token_ring.py 5003 5001
#    (second argument = next process in the ring)
# 4. The first process starts with the token.
# 5. Type 'cs' to enter the critical section.
# ============================================================

import socket
import threading
import sys
import time

HOST = 'localhost'
my_port = int(sys.argv[1])
next_port = int(sys.argv[2])
has_token = True if my_port == 5001 else False

def listener():
    global has_token
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, my_port))
    print(f"[Process {my_port}] Listening...")
    while True:
        data, addr = s.recvfrom(1024)
        msg = data.decode()
        if msg == 'TOKEN':
            has_token = True
            print(f"[{my_port}] Received TOKEN!")

def pass_token():
    global has_token
    has_token = False
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto('TOKEN'.encode(), (HOST, next_port))
    print(f"[{my_port}] Passed TOKEN to {next_port}")

def critical_section():
    global has_token
    if has_token:
        print(f"[{my_port}] Entered Critical Section!")
        time.sleep(3)
        print(f"[{my_port}] Exiting Critical Section.")
        pass_token()
    else:
        print(f"[{my_port}] No TOKEN — cannot enter CS now.")

threading.Thread(target=listener, daemon=True).start()

while True:
    cmd = input("Type 'cs' to enter Critical Section: ")
    if cmd.lower() == 'cs':
        critical_section()
