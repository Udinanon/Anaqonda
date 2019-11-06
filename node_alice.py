from cqc.pythonLib import CQCConnection, qubit
import random
import json
import time

N_QUBIT = 10

with CQCConnection("Alice") as Alice:
    # Preparing my qubits
    h_vector = [random.choice([0, 1]) for _ in range (N_QUBIT)]
    x_vector = [random.choice([0, 1]) for _ in range (N_QUBIT)]
    q_vector = []
    
    for _ in range(N_QUBIT):
        q_vector.append(qubit(Alice))
    
    for i in range(N_QUBIT):
        if x_vector[i] == 1:
            q_vector[i].X()
        if h_vector[i] == 1:
            q_vector[i].H()
    
    # Ask to Charlie (the commutor node as chosen for the network architecture)
    # if I am the master, stating who I am
    print("# Am I the master, stating who I am ?_?")
    Alice.sendClassical("Charlie", json.dumps( {"name": "Alice"} ).encode("utf-8"))
    charlie_attempt_response = Alice.recvClassical()
    im_master = json.loads(charlie_attempt_response.decode("utf-8"))
    
    # If Charlie responded than it's ready for receiving my qubits, I send them
    print("# I'm sending the qubits to Charlie T_T")
    for qubit in q_vector:
        Alice.sendQubit(qubit, "Charlie")
    
    # Receive the resulting matrix from Charlie
    matrix = json.loads(Alice.recvClassical().decode("utf-8"))

    time.sleep(1)

    # Send vector H
    Alice.sendClassical("Bob", json.dumps(h_vector).encode("utf-8"))

    # Read vector H
    hother_vector = json.loads(Alice.recvClassical().decode("utf-8"))

    if im_master:
        # Flips the necessary bits based on matrix correlation
        for i in range(N_QUBIT):
            if matrix[i][1] == 0:
                x_vector[i] = "b"
                continue
            if h_vector[i] != hother_vector[i]:
                x_vector[i] = "h"
                continue
            if h_vector[i] == 1 and matrix[i][0] == 0:
                continue
            x_vector[i] = 1 if x_vector[i] == 0 else 0

    else:
        pass  # nothing to do
    
    # Print the key obtained
    print(x_vector)

