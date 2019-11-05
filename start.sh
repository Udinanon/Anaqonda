simulaqron reset 
simulaqron set max-qubits 65536

simulaqron start --nodes Alice,Bob,Charlie 

python node_charlie.py &
python node_alice.py &
python node_bob.py &
