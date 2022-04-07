import random

class RandomPlayer:

	def __init__(self):
		print("Hello from <RandomAI>")

	def play(self, white, moves):
		r = True
		if bool([a for a in moves.values() if a != []]):
			while r:
				key = random.choice(list(moves))
				if len(moves[key]) > 0:
					r = False
			#print("Played")
			return (key,random.choice(moves[key]))
		else:
			print("Bye Bye from <RandomAI>")
		
		
		