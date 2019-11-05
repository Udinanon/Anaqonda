from cqc.pythonLib import CQCConnection, qubit
import json

def main():
	with CQCConnection("Charlie") as Charlie:
		
		qA=[]
		qB=[]
		
		#ricevi array Alice, array Bob
		for i in range(2*n):
			qI=Bob.recvQubit()
			if qI._qID.startswith("Alice"):
				qA.append(qI)
			else:
				qB.append(qI)
		
		#per ogni qubit fai cNOT , Alice.cNOT(BOB)
		for i in range(len(qA)):
			qA[i].cnot(qB[i])
		
		#Hadamard su array Alice
		for i in range(len(qA)):
			qA[i]=qA[i].H()
		#misura array Alice e Bob, Alice->vettore_successo, Bob->segno
		#creo matrice risultati, [succ, segno]
		M_out=[]
		for i in range(len(qA)):
			M_out.append([qA[i].measure(), qB[i].measure()])
		#invia matrice ad Alice e Bob
		print("CHARLIE IS DONE")
		print("HERE IS OUTPUT MATRIX: "+str(M_out))
		msg = json.dumps(M_out).encode('utf-8')
		Charlie.sendClassical(name="Alice", msg=msg)
		Charlie.sendClassical(name="Bob", msg=msg)
		

main()
