Device-Independent Quantum Key Distribution
=========

Node Charlie operations
---------
1. Wait for a request from one node
2. Tells him that will be the master(1)
3. Receive the qubits from the first node
4. Wait for a request from the second node
5. Tells him that will _not_ be the master(1)
6. Receive the qubits from the second node
7. Apply a cNOT on every qubit using the master's qubits as controller and the other node's qubits as target (2)
8. Apply the Hadamard to every qubit of the master (3)
9. Measure the qubits and send the results as an array of pairs to both the first and second node via a classical channel

Node Alice/Bob operations
---------
1. Generate two array (`x_vector` and `h_vector`) of random classical bits
2. Generate an array of qubits `q_vector` using the two classical vectors(4)
3. Send a request to Charlie
4. Receive if it will be the master
5. Send the qubits to Charlie
6. Wait for the matrix from Charlie
7. Exchange the `h_vector` with the other node
8. If the node is master it filters the `x_vector` in order to obtain the actual key(5)
9. Otherwise it cleans the unusable bits from the `x_vector`(6)

Notes
---------

(1) master: the node who flips the bits to recover the correct key

(2) Charlie's cNOT operation:
```python
first_node_qubits[i].cnot(second_node_qubits[i])
```

(3) Charlie's Hadamard operation:
```python
first_node_qubits[i].H()
```

(4) generation of the qubits:
```python
if x_vector[i] == 1:
    q_vector[i].X()  # Applies the X Gate
if h_vector[i] == 1:
    q_vector.H()  # Applies the Hadamard Gate
```

(5) filtering of the `x_vector`:
```python
if matrix[i][1] == 0:
    x_vector[i] = "b"
    continue
if h_vector[i] != hother_vector[i]:
    x_vector[i] = "h"
    continue
if h_vector[i] == 1 and matrix[i][0] == 0:
    continue
x_vector[i] = 1 if x_vector[i] == 0 else 0
```

(6) unusable bits removal from `x_vector`:
```python
if matrix[i][1] == 0:
    x_vector[i] = "b"
    continue
if h_vector[i] != hother_vector[i]:
    x_vector[i] = "h"
    continue
```
