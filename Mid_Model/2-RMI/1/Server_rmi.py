# ============================================================
# SERVER CODE (server_rmi.py)
# ============================================================
# AIM:
# To implement Remote Method Invocation (RMI) using Pyro4 so that
# methods can be executed remotely by a client.
#
# PROCEDURE TO EXECUTE:
# 1. Install Pyro4 (only once):   pip install Pyro4
# 2. Save this file as "server_rmi.py".
# 3. Open a terminal and run:    python -m Pyro4.naming
#    --> This starts the Pyro4 Name Server (keep it running).
# 4. Open a new terminal and run this server code:
#       python server_rmi.py
#    --> The server will register a Calculator object and wait for clients.
# 5. The URI of the service will be displayed in the terminal.
# 6. Copy the URI and use it in the client program when prompted.
# ============================================================

import Pyro4

# Step 1: Define Remote Service (Calculator class)
@Pyro4.expose
class Calculator:
    def add_numbers(self, a, b):
        """Add two numbers."""
        return a + b

    def multiply_numbers(self, a, b):
        """Multiply two numbers."""
        return a * b

# Step 2: Server Setup — Register the service with Pyro4 Daemon
daemon = Pyro4.Daemon()  # Create a Pyro daemon
uri = daemon.register(Calculator)  # Register the Calculator class
print("Calculator service is ready.")
print(f"URI to use in client: {uri}")  # Display URI for the client

# Step 3: Keep the server running to listen for client requests
print("Waiting for client requests...")
daemon.requestLoop()
