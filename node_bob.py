from cqc.pythonLib import *
import random

def main():
        
    with CQCConnection("Bob") as Bob:
        print("BOB READY")
        charlie_ok = Bob.recvClassical()

        print("BOB STARTED")
		
        #Set arrays with random values
        h_vector = [random.choice([0,1]) for _ in range(10)]
        x_vector = [random.choice([0,1]) for _ in range(10)]
		
        #Set qubit array
        q_vector = []
        for i in range(10):
            q_vector.append(qubit(Bob))
			
        #Set qubit coding using the random arrays
        for i in range(10):
            if x_vector[i] == 1:
                q_vector[i].X()
            if h_vector == 1:
                q_vector[i].H()
				
        #Send qubits
        for qbit in q_vector:
            Bob.sendQubit(qbit, "Charlie")
        print("BOB DONE")

        #Receive array from Charlie
        charlie_output = Bob.recvClassical()
        
        print("BOB X:"+str(x_vector))
        print("BOB H:"+str(h_vector))        

main()
