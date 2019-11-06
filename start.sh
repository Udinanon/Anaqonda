simulaqron stop
simulaqron reset
simulaqron set max-qubits 65536
#simulaqron set log-level 10
simulaqron start

python3 mdi_alice.py &
python3 mdi_bob.py &
python3 mdi_server.py 
