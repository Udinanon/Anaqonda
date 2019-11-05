from cqc.pythonLib import *
import random
def main():
		
	with CQCConnection("Alice") as Alice:
		h_vector = [random.choice([0,1]) for _ in range(10)]
		x_vector = [random.choice([0,1]) for _ in range(10)]

		q_vector = []
		for i in range(10):
			q_vector.append(qubit(Alice))

		for i in range(10):
			if x_vector[i] == 1:
				q_vector[i].X()
			if h_vector == 1:
				q_vector[i].H()

		print(q_vector)

main()
