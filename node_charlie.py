from cqc.pythonLib import CQCConnection, qubit
import json

def main():
    qA=[]
    qB=[]
    with CQCConnection("Charlie") as Charlie:
        print("CHARLIE STARTED")
        for i in range(10):
            qI=Charlie.recvQubit()
            qA.append(qI)
        print("CHARLIE RECEIVED ALICE")
        #Charlie.recvClassical()
        Charlie.sendClassical("Bob", 1)
        
        for i in range(10):
            qI=Charlie.recvQubit()
            qB.append(qI)
        print("CHARLIE RECEIVED BOB")
        print(len(qA))
        print(len(qB))
        
        #For every received qubit do cNOT operation, i.e. Alice.cNOT(Bob)
        for i in range(len(qA)):
            qA[i].cnot(qB[i])
        
        #Apply Hadamard transformation on Alice's array
        for i in range(len(qA)):
            qA[i].H()
		
		#Do the measurement on Alice and Bob arrays: Alice->success array, Bob->sign array
        #create results matrix, [succ, sign]
        M_out=[]
        for i in range(len(qA)):
            a=qA[i].measure()
            b=qB[i].measure()
            print("A:"+str(a))
            print("B:"+str(b))
            M_out.append([a, b])
			
        #Send results matrix to Alice and Bob
        print("CHARLIE IS DONE")
        print("HERE IS OUTPUT MATRIX: "+str(M_out))
        msg = json.dumps(M_out).encode('utf-8')
        Charlie.sendClassical(name="Alice", msg=msg)
        Charlie.sendClassical(name="Bob", msg=msg)

main()
