#########################################################################
#																		#
#				ChessGame (Tyche) 						  	v1.0.0 		#
#																		#
#	Author											   Hugo Masson		#
#																		#
#	Last Modified (eu date format)						06/04/2022		#
#																		#
#																		#
#	You are free to use this programm as you want						#
#	if you wish to repost a modified version please put a link			#
#	to my Github														#
#					https://github.com/HugoMasson?tab=repositories		#
#																		#
#########################################################################



import game_gui.gui as gui
import players.randomPlayer as ai

def main():
	print("Creating game instance...")
	g = gui.Gui(800, ai.RandomPlayer())
	print("Game instance created")
	g.init()
	print("Window init successful")
	g.run()

if __name__ == '__main__':
	print("Launching...")
	main()
	print("Bye")
