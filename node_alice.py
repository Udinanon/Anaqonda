from cqc.pythonLib import *
import random
import json
def main():
        
    with CQCConnection("Alice") as Alice:
        n=10

        hA_vector = [random.choice([0,1]) for _ in range(10)]
        xA_vector = [random.choice([0,1]) for _ in range(10)]
        hB_vector = [random.choice([0,1]) for _ in range(10)]
        xB_vector = [random.choice([0,1]) for _ in range(10)]

        qA_vector = []
        qB_vector = []
        for i in range(n):
            qA_vector.append(qubit(Alice))
            qB_vector.append(qubit(Alice))

        for i in range(n):
            if xA_vector[i] == 1:
                qA_vector[i].X()
            if hA_vector == 1:
                qA_vector[i].H()
            if xB_vector[i] == 1:
                qB_vector[i].X()
            if hB_vector == 1:
                qB_vector[i].H()

        for qbit in qA_vector:
            Alice.sendQubit(qbit, "Charlie")
        print("gjgk")

        for qbit in qB_vector:
            Alice.sendQubit(qbit, "Charlie")
        print("ACACA")

        charlie_output=Alice.recvClassical()
        M=json.loads(charlie_output.decode("utf-8"))

        print("ha:", end="")
        print(hA_vector)
        print("hb:", end="")
        print(hB_vector)
        print("xa:", end="")
        print(xA_vector)
        print("xb:", end="")
        print(xB_vector)
        print()
        for i in range(n):                
            if M[i][0] == 1 or hA_vector[i] != hB_vector[i]:
                xA_vector[i] = -1
                #hA_vector[i] = -1
                xB_vector[i] = -1
                #hB_vector[i] = -1
                continue
            if M[i][1] == 1 and hA_vector[i] == 1:
                continue
            xA_vector[i] = 1 if xA_vector[i] == 0 else 0
        
        print("ha:", end="")
        print(hA_vector)
        print("hb:", end="")
        print(hB_vector)
        print("xa:", end="")
        print(xA_vector)
        print("xb:", end="")
        print(xB_vector)


main()
