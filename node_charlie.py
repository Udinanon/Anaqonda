# https://softwarequtech.github.io/SimulaQron/html/_modules/cqc/pythonLib.html#qubit

from cqc.pythonLib import CQCConnection, qubit
import json

def main():
    
    qA=[]
    qB=[]

    with CQCConnection("Charlie") as CharlieA:
        for i in range(10):
            qI=CharlieA.recvQubit()
            qA.append(qI)

    with CQCConnection("Eve") as CharlieB:
        for i in range(10):
            qI=CharlieB.recvQubit()
            qB.append(qI)
    
    print(qA)
    print(qB)

main()