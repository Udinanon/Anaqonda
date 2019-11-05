from cqc.pythonLib import *
import random

def main():
        
    with CQCConnection("Bob") as Bob:
        print("BOB READY")
        charlie_ok = Bob.recvClassical()

        print("BOB STARTED")
        #array random
        h_vector = [random.choice([0,1]) for _ in range(10)]
        x_vector = [random.choice([0,1]) for _ in range(10)]
        #array qubit
        q_vector = []
        for i in range(10):
            q_vector.append(qubit(Bob))
        #codifica valori in qubit
        for i in range(10):
            if x_vector[i] == 1:
                q_vector[i].X()
            if h_vector == 1:
                q_vector[i].H()
        #invia qubit
        for qbit in q_vector:
            Bob.sendQubit(qbit, "Charlie")
        print("BOB DONE")

        #ricevo c_vector
        charlie_output = Bob.recvClassical()
        
        print("BOB X:"+str(x_vector))
        print("BOB H:"+str(h_vector))
        # !SERVER#se c[i][0]==0 lo scarto, se ==1 tengo
        # allora predno c[i][1] e prendo h_vector
        # h==0 flippo x[i], h==1 e c[i][1]==1 flippo, altrimenti lascio
        # confronta x_bob e x_alice, se uguali alora siamo a posto
        

main()
