from cqc.pythonLib import CQCConnection, qubit
import random
import json
import time

N_QUBIT = 100

with CQCConnection("Bob") as Bob:
    # Preparing my qubits
    h_vector = [random.choice([0, 1]) for _ in range (N_QUBIT)]
    x_vector = [random.choice([0, 1]) for _ in range (N_QUBIT)]
    q_vector = []
    
    for _ in range(N_QUBIT):
        q_vector.append(qubit(Bob))
    
    for i in range(N_QUBIT):
        if x_vector[i] == 1:
            q_vector[i].X()
        if h_vector[i] == 1:
            q_vector[i].H()
    
    # Ask to Charlie (the commutor node as chosen for the network architecture)
    # if I am the master, stating who I am
    print("# Am I the master, stating who I am ?_?")
    Bob.sendClassical("Charlie", json.dumps( {"name": "Bob"} ).encode("utf-8"))
    charlie_attempt_response = Bob.recvClassical()
    im_master = json.loads(charlie_attempt_response.decode("utf-8"))
    
    # If Charlie responded than it's ready for receiving my qubits, I send them
    print("# I'm sending the qubits to Charlie T_T")
    for qubit in q_vector:
        Bob.sendQubit(qubit, "Charlie")
    
    # Receive the resulting matrix from Charlie
    matrix = json.loads(Bob.recvClassical().decode("utf-8"))

    time.sleep(1)

    # Read vector H
    hother_vector = json.loads(Bob.recvClassical().decode("utf-8"))

    # Send vector H
    Bob.sendClassical("Alice", json.dumps(h_vector).encode("utf-8"))

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
        # Remove errors
        for i in range(N_QUBIT):
            if matrix[i][1] == 0:
                x_vector[i] = "b"
                continue
            if h_vector[i] != hother_vector[i]:
                x_vector[i] = "h"
                continue

    # Filtering key
    key = []
    for i in range(N_QUBIT):
        if type(x_vector[i]) is not str:
            key.append(x_vector[i])

    # Print the key obtained
    print(key)
    print("Key length" + str(len(key)))

    # TOremove
    #xother_vector = json.loads(Bob.recvClassical().decode("utf-8"))

    #error_counts = 0
    #for i in range(N_QUBIT):
    #    if x_vector[i] != xother_vector[i]:
    #        error_counts += 1
    #print("Errors = " + str(error_counts))

