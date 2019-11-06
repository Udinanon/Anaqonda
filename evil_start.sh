simulaqron reset
simulaqron set max-qubits 65536
simulaqron start

python3 node_evil_charlie.py &
python3 node_alice.py &
python3 node_bob.py
