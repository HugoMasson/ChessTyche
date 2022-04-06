from copy import deepcopy	#to copy a 2d array

WHITE_PLAYER = 2
BLACK_PLAYER = 1

class Board:

	def __init__(self):
		self.wKingMoved = False
		self.bKingMoved = False
		self.wRooksMoved = [False, False]
		self.bRooksMoved = [False, False]
		self.pieces = {
			11:"assets/images/white_pawn.png",
			12:"assets/images/white_king.png",
			13:"assets/images/white_knight.png",
			14:"assets/images/white_bishop.png",
			15:"assets/images/white_rook.png",
			19:"assets/images/white_queen.png",
			21:"assets/images/black_pawn.png",
			22:"assets/images/black_king.png",
			23:"assets/images/black_knight.png",
			24:"assets/images/black_bishop.png",
			25:"assets/images/black_rook.png",
			29:"assets/images/black_queen.png",
		}
		"""
		self.board = [
			[25,23,24,29,22,24,23,25],
			[21,21,21,21,21,21,21,21],
			[00,00,00,00,00,00,00,00],
			[00,00,00,00,00,00,00,00],
			[00,00,00,00,00,00,00,00],
			[00,00,00,00,00,00,00,00],
			[11,11,11,11,11,11,11,11],
			[15,13,14,19,12,14,13,15],
		]
		"""
		self.board = [
			[25,00,00,21,22,00,00,25],
			[00,21,00,00,00,00,00,00],
			[00,00,00,00,00,00,00,00],
			[00,00,00,00,00,00,00,00],
			[00,00,00,00,00,00,00,00],
			[00,00,00,00,00,00,00,00],
			[00,00,11,00,00,00,11,00],
			[00,00,00,00,12,00,00,00],
		]
		
	def getBoard(self):
		return self.board
	def getPieces(self):
		return self.pieces
	def swap(self, x, y, x2, y2, arr="default"):
		if arr == "default":
			arr = self.board
		arr[x2][y2] = arr[x][y]
		arr[x][y] 	= 0
		return arr
	
	def whereIsKing(self, white, arr="default"):
		if arr == "default":
			arr = self.board
		for i in range(8):
			for j in range(8):
				if arr[i][j] == 12 and white:
					return i,j
				elif arr[i][j] == 22 and (not white):
					return i,j

	def isInBoard(self, x, y):
		return x >= 0 and x <= 7 and y >= 0 and y <= 7 

	def isWhitePiece(self, x, y, arr="default"):
		if arr == "default":
			arr = self.board
		return arr[x][y] < 20 and arr[x][y] != 0

	def getColor(self, piece):		#true: white / false: black
		if piece > 20:
			return False
		elif piece < 20 and piece != 0:
			return True
		return None

	def isBlackPiece(self, x, y, arr="default"):
		if arr == "default":
			arr = self.board
		return arr[x][y] > 20

	def coordToStandard(self, x, y):	#ex: 6 0 -> a2 
		return str(chr(97+y)+""+str(8-x))

	def standardToCoord(self, expr):	#ex: a2 -> 6 0
		return (8-int(expr[1]), ord(expr[0])-97)

	def move(self, x, y, x2, y2, white, arr="default"):		#working
		if arr == "default":
			arr = self.board

		if self.isWhitePiece(x2, y2, arr) and self.isWhitePiece(x, y, arr):
			return False
		if self.isBlackPiece(x2, y2, arr) and self.isBlackPiece(x, y, arr):
			return False
		
		key = self.coordToStandard(x, y)
		legalMoves = self.getLegalMoves(white, arr)
		if key in legalMoves:
			if self.coordToStandard(x2, y2) in legalMoves[key]:
				if   arr[x][y] == 12:
					self.wKingMoved = True
					if y == y2+2 and arr[x][y+1] == 0 and arr[x][y+2] == 0:
						arr[x2][y2+1] = arr[x][y-4]
						arr[x][y-4] = 0
					elif y == y2-2 and arr[x][y-1] == 0 and arr[x][y-2] == 0:
						arr[x2][y2-1] = arr[x][y+3]
						arr[x][y+3] = 0
				elif arr[x][y] == 22:
					self.bKingMoved = True
					if y == y2+2 and arr[x][y+1] == 0 and arr[x][y+2] == 0:
						arr[x2][y2+1] = arr[x][y-4]
						arr[x][y-4] = 0
					elif y == y2-2 and arr[x][y-1] == 0 and arr[x][y-2] == 0:
						arr[x2][y2-1] = arr[x][y+3]
						arr[x][y+3] = 0
				elif arr[x][y] == 15:
					if x == 7 and y == 0:
						self.wRooksMoved[0] = True
					elif x == 7 and y == 7:
						self.wRooksMoved[1] = True
				elif arr[x][y] == 25:
					if x == 0 and y == 0:
						self.bRooksMoved[0] = True
					elif x == 0 and y == 7:
						self.bRooksMoved[1] = True
				

				arr[x2][y2] = arr[x][y]
				arr[x][y]	= 0
				if arr[x2][y2] == 11 and x2 == 0:
					arr[x2][y2] = 19
				elif arr[x2][y2] == 21 and x2 == 7:
					arr[x2][y2] = 29
				return True

		return False

	def isPlaceable(self, piece, x, y, arr="default"):		#working
		if self.isInBoard(x, y):
			if arr == "default":
				arr = self.board
			if piece > 20 and arr[x][y] < 20:
				return True
			elif (piece < 20 and piece > 0 and arr[x][y] > 20 or  arr[x][y] == 0):
				return True
		return False 

	def isAttacked(self, x, y, white, moves, arr="default"):	#working
		if arr == "default":
			arr = self.board

		target = self.coordToStandard(x, y)
		for key in moves:
			for m in moves[key]:
				if m == target:
					return True
		return False

	def getAllPawnMoves(self, x, y, white, arr="default"):		#working
		if arr == "default":
			arr = self.board
		direction = 1
		if white:
			direction = -1

		moves = []

		#standard
		if self.isInBoard(x+direction, y) and arr[x+direction][y] == 0:
			moves.append(self.coordToStandard(x+direction, y))
			if self.isInBoard(x+2*direction, y) and arr[x+2*direction][y] == 0 and (x == 1 and (not white) or x == 6 and white):
				moves.append(self.coordToStandard(x+2*direction, y))

		#take
		if self.isInBoard(x+direction, y+1):
			if white and self.isBlackPiece(x+direction,y+1,arr)  or (not white) and self.isWhitePiece(x+direction,y+1,arr):
				moves.append(self.coordToStandard(x+direction, y+1))
		if self.isInBoard(x+direction, y-1):
			if white and self.isBlackPiece(x+direction,y-1,arr)  or (not white) and self.isWhitePiece(x+direction,y-1,arr):
				moves.append(self.coordToStandard(x+direction, y-1))
		return moves

	def getAllBishopMoves(self, x, y, white, arr="default"):	#working
		if arr == "default":
			arr = self.board

		moves = []
		tl, tr, bl, br = True, True, True, True
		count = 1
		while tl or tr or bl or br:
			if tl:
				if x-count >= 0 and y-count >= 0 and self.isPlaceable(arr[x][y], x-count, y-count, arr):
					moves.append(self.coordToStandard(x-count, y-count))
					if self.getColor(arr[x-count][y-count]) == (not white):
						tl = False
				else:
					tl = False
			if tr:
				if x-count >= 0 and y+count <= 7 and self.isPlaceable(arr[x][y], x-count, y+count, arr):
					moves.append(self.coordToStandard(x-count, y+count))
					if self.getColor(arr[x-count][y+count]) == (not white):
						tr = False
				else:
					tr = False
			if bl:
				if x+count <= 7 and y-count >= 0 and self.isPlaceable(arr[x][y], x+count, y-count, arr):
					moves.append(self.coordToStandard(x+count, y-count))
					if self.getColor(arr[x+count][y-count]) == (not white):
						bl = False
				else:
					bl = False
			if br:
				if x+count <= 7 and y+count <= 7 and self.isPlaceable(arr[x][y], x+count, y+count, arr):
					moves.append(self.coordToStandard(x+count, y+count))
					if self.getColor(arr[x+count][y+count]) == (not white):
						br = False
				else:
					br = False
			count += 1
		return moves

	def getAllRookMoves(self, x, y, white, arr="default"):		#working
		if arr == "default":
			arr = self.board

		moves = []
		top, bot, left, right = True, True, True, True
		count = 1
		while top or bot or left or right:
			if left:
				if y-count >= 0 and self.isPlaceable(arr[x][y], x, y-count, arr):
					moves.append(self.coordToStandard(x, y-count))
					if self.getColor(arr[x][y-count]) == (not white):
						left = False
				else:
					left = False

			if right:
				if y+count <= 7 and self.isPlaceable(arr[x][y], x, y+count, arr):
					moves.append(self.coordToStandard(x, y+count))
					if self.getColor(arr[x][y+count]) == (not white):
						right = False
				else:
					right = False
			if top:
				if x-count >= 0 and self.isPlaceable(arr[x][y], x-count, y, arr):
					moves.append(self.coordToStandard(x-count, y))
					if self.getColor(arr[x-count][y]) == (not white):
						top = False
				else:
					top = False
			if bot:
				if x+count <= 7 and self.isPlaceable(arr[x][y], x+count, y, arr):
					moves.append(self.coordToStandard(x+count, y))
					if self.getColor(arr[x+count][y]) == (not white):
						bot = False
				else:
					bot = False
			count += 1
		return moves

	def getAllQueenMoves(self, x, y, white, arr="default"):		#working
		return self.getAllRookMoves(x, y, white, arr) + self.getAllBishopMoves(x, y, white, arr)

	def getAllKnightMoves(self, x, y, white, arr="default"):	#working
		if arr == "default":
			arr = self.board

		moves = []
		if self.isInBoard(x+2, y+1) and self.isPlaceable(arr[x][y], x+2, y+1, arr):
			moves.append(self.coordToStandard(x+2, y+1))
		if self.isInBoard(x+2, y-1) and self.isPlaceable(arr[x][y], x+2, y-1, arr):
			moves.append(self.coordToStandard(x+2, y-1))
		if self.isInBoard(x-2, y+1) and self.isPlaceable(arr[x][y], x-2, y+1, arr):
			moves.append(self.coordToStandard(x-2, y+1))
		if self.isInBoard(x-2, y-1) and self.isPlaceable(arr[x][y], x-2, y-1, arr):
			moves.append(self.coordToStandard(x-2, y-1))
		if self.isInBoard(x+1, y+2) and self.isPlaceable(arr[x][y], x+1, y+2, arr):
			moves.append(self.coordToStandard(x+1, y+2))
		if self.isInBoard(x+1, y-2) and self.isPlaceable(arr[x][y], x+1, y-2, arr):
			moves.append(self.coordToStandard(x+1, y-2))
		if self.isInBoard(x-1, y+2) and self.isPlaceable(arr[x][y], x-1, y+2, arr):
			moves.append(self.coordToStandard(x-1, y+2))
		if self.isInBoard(x-1, y-2) and self.isPlaceable(arr[x][y], x-1, y-2, arr):
			moves.append(self.coordToStandard(x-1, y-2))

		return moves

	def getAllKingMoves(self, x, y, white, arr="default"):		#working (not rock)
		if arr == "default":
			arr = self.board

		moves = []

		if self.isInBoard(x+1, y) and self.isPlaceable(arr[x][y], x+1, y, arr):
			moves.append(self.coordToStandard(x+1, y))
		if self.isInBoard(x+1, y+1) and self.isPlaceable(arr[x][y], x+1, y+1, arr):
			moves.append(self.coordToStandard(x+1, y+1))
		if self.isInBoard(x+1, y-1) and self.isPlaceable(arr[x][y], x+1, y-1, arr):
			moves.append(self.coordToStandard(x+1, y-1))
		if self.isInBoard(x-1, y) and self.isPlaceable(arr[x][y], x-1, y, arr):
			moves.append(self.coordToStandard(x-1, y))
		if self.isInBoard(x-1, y+1) and self.isPlaceable(arr[x][y], x-1, y+1, arr):
			moves.append(self.coordToStandard(x-1, y+1))
		if self.isInBoard(x-1, y-1) and self.isPlaceable(arr[x][y], x-1, y-1, arr):
			moves.append(self.coordToStandard(x-1, y-1))
		if self.isInBoard(x, y+1) and self.isPlaceable(arr[x][y], x, y+1, arr):
			moves.append(self.coordToStandard(x, y+1))
		if self.isInBoard(x, y-1) and self.isPlaceable(arr[x][y], x, y-1, arr):
			moves.append(self.coordToStandard(x, y-1))

		if white:
			if not self.wKingMoved:
				if not self.wRooksMoved[0] and arr[x][y-4] == 15:
					moves.append(self.coordToStandard(x, y-2))
				if not self.wRooksMoved[1] and arr[x][y+3] == 15:
					moves.append(self.coordToStandard(x, y+2))
		else:
			if not self.bKingMoved:
				if not self.bRooksMoved[0] and arr[x][y-4] == 25:
					moves.append(self.coordToStandard(x, y-2))
				if not self.bRooksMoved[1] and arr[x][y+3] == 25:
					moves.append(self.coordToStandard(x, y+2))
		return moves
		
	def getPotentialMoves(self, white, arr="default"):			#working
		potentialMoves = {}

		if arr == "default":
			arr = self.board

		adjuster = 0
		if not white:
			adjuster = -10

		for x in range(len(arr)):
			for y in range(len(arr[x])):
				p = arr[x][y] + adjuster
				key = self.coordToStandard(x, y)

				if   p == 11:		#Pawn
					potentialMoves[key] = self.getAllPawnMoves(x, y, white, arr)
				elif p == 14:		#Bishop
					potentialMoves[key] = self.getAllBishopMoves(x, y, white, arr)
				elif p == 13:		#Knight
					potentialMoves[key] = self.getAllKnightMoves(x, y, white, arr)
				elif p == 15:		#Rook
					potentialMoves[key] = self.getAllRookMoves(x, y, white, arr)
				elif p == 19:		#Queen
					potentialMoves[key] = self.getAllQueenMoves(x, y, white, arr)
				elif p == 12:		#King
					potentialMoves[key] = self.getAllKingMoves(x, y, white, arr)


		return potentialMoves

	#return list of all the possible moves for a position
	def getLegalMoves(self, white, arr="default"):
		legalMoves = {}
		if arr == "default":
			arr = self.board

		cArr = deepcopy(arr)
		moves = self.getPotentialMoves(white, arr)
		a = 0
		#print(moves)
		for key in moves:
			
			legalMoves[key] = []
			for m in moves[key]:

				cArr = deepcopy(arr)
				
				a    += 1
				c    = self.standardToCoord(key)
				c2   = self.standardToCoord(m)
				val  = cArr[c2[0]][c2[1]]
				cArr = self.swap(c[0], c[1], c2[0], c2[1], cArr)	#play the 'm' move

				king = self.whereIsKing(white, cArr)

				moves2 = self.getPotentialMoves(not white, cArr)
				if val != 0 and (cArr[c2[0]][c2[1]] == 22 or cArr[c2[0]][c2[1]] == 12):
					kStd   = self.coordToStandard(c2[0], c2[1])
					moves3 = self.getPotentialMoves(white, cArr)
					if not self.isAttacked(c2[0], c2[1], white, moves3, cArr):
						legalMoves[key].append(m)
					for kk in moves2:
						for mkk in moves2[kk]:
							if kStd == mkk:
								legalMoves[key].pop()
				else:
					if not self.isAttacked(king[0], king[1], not white, moves2, cArr):
						legalMoves[key].append(m)
						if cArr[c2[0]][c2[1]] == 12:
							if c[1]-c2[1] == 2:
								if self.isAttacked(c[0], c[1]-1, not white, moves2, cArr) or self.isAttacked(c[0], c[1]-2, not white, moves2, cArr) or self.isAttacked(c[0], c[1], not white, moves2, cArr):
									legalMoves[key].pop()
							elif c[1]-c2[1] == -2:
								if self.isAttacked(c[0], c[1]+1, not white, moves2, cArr) or self.isAttacked(c[0], c[1]+2, not white, moves2, cArr) or self.isAttacked(c[0], c[1], not white, moves2, cArr):
									legalMoves[key].pop()
						
						elif cArr[c2[0]][c2[1]] == 22:
							if c[1]-c2[1] == 2:
								if self.isAttacked(c[0], c[1]-1, not white, moves2, cArr) or self.isAttacked(c[0], c[1]-2, not white, moves2, cArr) or self.isAttacked(c[0], c[1], not white, moves2, cArr):
									legalMoves[key].pop()
							elif c[1]-c2[1] == -2:
								if self.isAttacked(c[0], c[1]+1, not white, moves2, cArr) or self.isAttacked(c[0], c[1]+2, not white, moves2, cArr) or self.isAttacked(c[0], c[1], not white, moves2, cArr):
									legalMoves[key].pop()

		#check mate / pat ... verifs (if no legal moves)
		if not bool([a for a in legalMoves.values() if a != []]):
			king   = self.whereIsKing(white, arr)
			moves4 = self.getPotentialMoves(not white, arr)
			if self.isAttacked(king[0], king[1], white, moves4, arr):
				print("Mate")
			else:
				print(king[0], king[1], moves, arr)

		return legalMoves

		


















			
