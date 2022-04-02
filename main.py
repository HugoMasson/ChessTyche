import game_gui.gui as gui





def main():
	print("Creating game instance...")
	g = gui.Gui(800)
	print("Game instance created")
	g.init()
	print("Window init successful")
	g.run()

if __name__ == '__main__':
	print("Launching...")
	main()
