import pygame
import os
import boardController

BLACK    = (125, 135, 150)
WHITE    = (232, 235, 239)
SELECTED = (123, 217, 100)

WHITE_PLAYER = True
BLACK_PLAYER = False

class Gui():

	def __init__(self, size):
		pygame.init()
		self.isW = WHITE_PLAYER
		self.font = pygame.font.SysFont(None, 24)
		self.bc = boardController.Board()
		self.size = size	#squae 8x8
		self.cSize = int(size/8)
		self.screen = None
		self.dirname = os.path.dirname(__file__)+"/../"	#right on ChessPyGame/ folder
		self.selected = [None, None]
		self.pieceSelected = False

	def stToCoorY(self, a):
		return 8-int(a)
	def stToCoorX(self, a):
		return ord(a)-97

	def init(self):
		self.screen = pygame.display.set_mode((self.size, self.size))
		pygame.display.set_caption('Chess Game')

	def draw(self):
		if self.isW:
			movesPossible = self.bc.getLegalMoves(WHITE_PLAYER)
		else:
			movesPossible = self.bc.getLegalMoves(BLACK_PLAYER)

		for i in range(8):
			for j in range(8):
				#draw pattern
				if (i+j) % 2 == 0:
					pygame.draw.rect(self.screen, WHITE, pygame.Rect(i*self.cSize, j*self.cSize, self.cSize, self.cSize))
				else:
					pygame.draw.rect(self.screen, BLACK, pygame.Rect(i*self.cSize, j*self.cSize, self.cSize, self.cSize))

				#draw selected tile
				if i == self.selected[0] and j == self.selected[1]:
					pygame.draw.rect(self.screen, SELECTED, pygame.Rect(i*self.cSize, j*self.cSize, self.cSize, self.cSize))

				#draw pieces
				if self.bc.getBoard()[j][i] != 0:
					self.screen.blit(pygame.transform.scale(pygame.image.load(self.dirname+self.bc.getPieces()[self.bc.getBoard()[j][i]]), (self.cSize, self.cSize)), (i*self.cSize, j*self.cSize))
		
		if self.selected[0] != None:

			#print(self.bc.isAttacked(self.selected[0], self.selected[1], self.isW))
			key = self.bc.coordToStandard(self.selected[1], self.selected[0])
			if key in movesPossible:
				for i in range(len(movesPossible[key])):
					pygame.draw.circle(self.screen, SELECTED, (int(self.stToCoorX(movesPossible[key][i][0])*self.cSize)+self.cSize/2, int(self.stToCoorY(movesPossible[key][i][1])*self.cSize)+self.cSize/2), self.cSize/5)

		#case pos
		for x in range(8):
			s = self.font.render(str(8-x), True, SELECTED)
			self.screen.blit(s, (5, x*self.cSize+5))
			s = self.font.render(chr(97+x), True, SELECTED)
			self.screen.blit(s, (x*self.cSize+0.5*self.cSize, 8*self.cSize-15))
		

		pygame.display.flip()


	def run(self):
		running = True
		while running:	
			for event in pygame.event.get():
				toRefresh = True
				if event.type == pygame.MOUSEBUTTONDOWN:
					
					pos = pygame.mouse.get_pos()
					tempA = int(pos[0]/self.cSize)
					tempB = int(pos[1]/self.cSize)
					if self.pieceSelected:
						if self.bc.move(self.selected[1], self.selected[0], tempB, tempA, self.isW):
							self.isW = not self.isW
						self.pieceSelected = False
					if self.selected[0] == None or (self.selected[0] != tempA or self.selected[1] != tempB):
						self.selected[0] = tempA
						self.selected[1] = tempB
						self.pieceSelected = False
						if self.bc.getBoard()[self.selected[1]][self.selected[0]] != 0:
							self.pieceSelected = True
					else:
						self.pieceSelected = False
						self.selected[0] = None
						self.selected[1] = None

					
				if event.type == pygame.QUIT:
					running = False
				self.draw()

			pygame.display.update()
		



