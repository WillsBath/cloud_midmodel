# ============================================================
# CLIENT CODE (client_rmi.py)
# ============================================================
# AIM:
# To connect to a remote Calculator service using Pyro4 and
# invoke methods (addition and multiplication) remotely.
#
# PROCEDURE TO EXECUTE:
# 1. Make sure the Pyro4 Name Server and server_rmi.py are running.
# 2. Save this file as "client_rmi.py".
# 3. Open a new terminal and run:   python client_rmi.py
# 4. When prompted, enter the URI shown by the server (e.g.,
#    PYRO:obj_1234567890abcdef@localhost:50500)
# 5. Enter two numbers when asked.
# 6. The client will call the remote add_numbers and multiply_numbers methods
#    and display the results.
# ============================================================

import Pyro4

# Step 1: Get the server URI from user
uri = input("Enter the server URI (as shown in server terminal): ")

# Step 2: Create a proxy object to connect to the remote service
calculator = Pyro4.Proxy(uri)

# Step 3: Take inputs from user
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

# Step 4: Invoke remote methods
sum_result = calculator.add_numbers(a, b)
product_result = calculator.multiply_numbers(a, b)

# Step 5: Display results
print("\n===== Remote Method Invocation Results =====")
print(f"Addition result: {sum_result}")
print(f"Multiplication result: {product_result}")
print("============================================")
