from cqc.pythonLib import CQCConnection, qubit

def main():
	with CQCConnection("Charlie") as Charlie:
		#ricevi array Alice, array Bob
		#per ogni qubit fai cNOT , Alice.cNOT(BOB)
		#Hadamard su array Alice
		#misura array Alice e Bob, Alice->vettore_successo, Bob->segno
		#creo matrice risultati, [succ, segno]
		#invia matrice ad Alice e Bob
		
		

main()
