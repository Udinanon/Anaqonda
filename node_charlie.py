# https://softwarequtech.github.io/SimulaQron/html/_modules/cqc/pythonLib.html#qubit

from cqc.pythonLib import CQCConnection, qubit
import json

def main():
    
    n=10
    qA=[]
    qB=[]

    with CQCConnection("Charlie") as Charlie:
        for i in range(n):
            qI=Charlie.recvQubit()
            qA.append(qI)
        
        for i in range(n):
            qI=Charlie.recvQubit()
            qB.append(qI)
        
        #-------------------------------------
        #per ogni qubit fai cNOT , Alice.cNOT(BOB)
        for i in range(len(qA)):
            qA[i].cnot(qB[i])
            
        #Hadamard su array Alice
        for i in range(len(qA)):
            qA[i].H()

        M_out=[]
        for i in range(len(qA)):
            M_out.append([qA[i].measure(), qB[i].measure()])
        print(M_out)

        Charlie.sendClassical("Alice", json.dumps(M_out).encode('utf-8'))
#        Charlie.sendClassical("Alice", M_out)
    #misura array Alice e Bob, Alice->vettore_successo, Bob->segno
    #creo matrice risultati, [succ, segno]
    

main()