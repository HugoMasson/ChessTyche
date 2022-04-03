from copy import deepcopy

WHITE_PLAYER = 2
BLACK_PLAYER = 1

class Board:

	def __init__(self):
		self.turn = 1
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
			[25,24,23,00,22,00,00,00],
			[00,00,00,00,00,00,00,00],
			[00,00,00,00,00,00,00,00],
			[00,00,00,00,00,00,00,00],
			[00,00,00,00,00,00,00,00],
			[00,00,00,00,00,00,00,00],
			[00,00,00,00,00,00,00,00],
			[15,14,13,00,12,00,00,00],
		]

	def whereIsKing(self, isW, arr="default"):
		if arr == "default":
			arr = self.board
		for i in range(8):
			for j in range(8):
				if arr[i][j] == 12 and isW:
					return i,j
				elif arr[i][j] == 22 and not isW:
					return i,j



	def isInBoard(self, x, y):
		return x >= 0 and x <= 7 and y >= 0 and y <= 7 

	def isWhiteTurn(self):
		return self.turn % 2 != 0

	def isBlackTurn(self):
		return self.turn % 2 == 0

	def isWhitePiece(self, x, y):
		return self.board[x][y] < 20 and self.board[x][y] != 0

	def isBlackPiece(self, x, y):
		return self.board[x][y] > 20

	def nextTurn(self):
		self.turn += 1

	def getBoard(self):
		return self.board

	def getPieces(self):
		return self.pieces

	def coordToStandard(self, x, y):	#ex: 6 0 -> a2 
		return str(chr(97+x)+""+str(8-y))


	def standardToCoord(self, expr):	#ex: a2 -> 6 0
		return (8-int(expr[1]), ord(expr[0])-97)


	def move(self, x, y, x2, y2, isW):
		if self.isWhitePiece(x2, y2) and self.isWhitePiece(x, y):
			return False
		if self.isBlackPiece(x2, y2) and self.isBlackPiece(x, y):
			return False
		
		movesAllowed = self.getAllMovesPossible(not isW)

		#is a move allowed
		v = list(movesAllowed.values())
		for i in range(len(v)):
			if self.coordToStandard(y2, x2) in v[i] and list(movesAllowed.keys())[i] == self.coordToStandard(y, x):
				if self.board[x][y] == 12 or self.board[x][y] == 22:	#king special moves (rock)
					if x == x2:
						if y == y2-2:
							self.board[x2][y2] = self.board[x][y]
							self.board[x2][y2-1] = self.board[x2][y2+1]
							self.board[x2][y2+1] = 0
							self.board[x][y] = 0
							if isW:
								self.wKingMoved = True
							else:
								self.bKingMoved = True
							return True
						elif y == y2+2:
							self.board[x2][y2] = self.board[x][y]
							self.board[x2][y2+1] = self.board[x2][y2-2]
							self.board[x2][y2-2] = 0
							self.board[x][y] = 0
							if isW:
								self.wKingMoved = True
							else:
								self.bKingMoved = True
							return True

				#vars used for rocks
				if self.board[x][y] == 12:
					self.wKingMoved = True
				elif self.board[x][y] == 22:
					self.bKingMoved = True
				elif self.board[x][y] == 15 and x == 7 and y == 0:
					self.wRooksMoved[0] = True
				elif self.board[x][y] == 15 and x == 7 and y == 7:
					self.wRooksMoved[1] = True
				elif self.board[x][y] == 25 and x == 0 and y == 0:
					self.bRooksMoved[0] = True
				elif self.board[x][y] == 25 and x == 0 and y == 7:
					self.bRooksMoved[1] = True
					
				self.board[x2][y2] = self.board[x][y]
				self.board[x][y] = 0
				return True
		return False

	def isPlaceable(self, piece, x, y):
		if piece < 20 and piece != 0:
			if self.isWhitePiece(x, y):
				return False
		else:
			if self.isBlackPiece(x, y):
				return False

	def isAttacked(self, x, y, attackColor, moves, arr):
		#attackColor = True -> mean white attack
		if attackColor:
			#moves = self.getAllMovesPossible(WHITE_PLAYER, False)
			v = list(moves.values())
			for i in range(len(v)):
				if self.coordToStandard(x, y) in v[i]:
					key = self.standardToCoord(list(moves.keys())[i])
					if arr[key[0]][key[1]] == 11 and y+1 <= 7 and (y+1, x) == key:	#if is a pawn advancing (not capture)
						pass
					else:
						#print("Attaker white: ", arr[key[0]][key[1]])
						return True
			if y+1 <= 7:
				if x+1 <= 7 and arr[y+1][x+1] == 11:
					return True
				if x-1 >= 0 and arr[y+1][x-1] == 11:
					return True
		else:
			#moves = self.getAllMovesPossible(BLACK_PLAYER)
			v = list(moves.values())
			for i in range(len(v)):
				if self.coordToStandard(x, y) in v[i]:
					key = self.standardToCoord(list(moves.keys())[i])
					if arr[key[0]][key[1]] == 21 and y-1 <= 7 and (y-1, x) == key:	#if is a pawn advancing (not capture)
						pass
					else:
						#print("Attaker black: ", self.coordToStandard(x, y), list(moves.keys())[i], v[i])
						return True
			if y+1 <= 7:
				if x+1 <= 7 and arr[y-1][x+1] == 21:
					return True
				if x-1 >= 0 and arr[y-1][x-1] == 21:
					return True
		return False


			

	def getAllPawnMoves(self, x, y, isW):	#pawn moves Ok
		#x: up / down y: right / left
		moves = []
		if isW:
			if x-1 >= 0:
				if self.board[x-1][y] == 0:
					moves.append(self.coordToStandard(y, x-1))
					if x == 6 and self.board[x-2][y] == 0:	#never moved
						moves.append(self.coordToStandard(y, x-2))
				if y-1 >= 0:
					if self.board[x-1][y-1] > 20:
						moves.append(self.coordToStandard(y-1, x-1))
				if y+1 <= 7:
					if self.board[x-1][y+1] > 20:
						moves.append(self.coordToStandard(y+1, x-1))
		else:
			if x+1 <= 7:
				if self.board[x+1][y] == 0:
					moves.append(self.coordToStandard(y, x+1))
					if x == 1 and self.board[x+2][y] == 0:	#never moved
						moves.append(self.coordToStandard(y, x+2))
				if y-1 >= 0:
					if self.board[x+1][y-1] < 20 and self.board[x+1][y-1] != 0:
						moves.append(self.coordToStandard(y-1, x+1))
				if y+1 <= 7:
					if self.board[x+1][y+1] < 20 and self.board[x+1][y+1] != 0:
						moves.append(self.coordToStandard(y+1, x+1))
		
		return moves

	def getAllBishopMoves(self, x, y, isW):		#to refactor if wanted on one while (with cond has To Continue Checking top right for ex)
		moves = []
		tx = x
		ty = y
		#down left
		while tx+1 <= 7 and ty-1 >= 0:
			tx+=1
			ty-=1
			#black encounter black or white encounter white
			if (self.board[tx][ty] > 20 and not isW) or (self.board[tx][ty] > 10 and self.board[tx][ty] < 20 and self.board[tx][ty] != 0 and isW):
				break
			else:
				moves.append(self.coordToStandard(ty, tx))
				if (self.board[tx][ty] > 20 and isW) or (self.board[tx][ty] < 20 and self.board[tx][ty] != 0 and not isW):
					break
		tx = x
		ty = y
		#down right
		while tx+1 <= 7 and ty+1 <= 7:
			tx+=1
			ty+=1
			#black encounter black or white encounter white
			if (self.board[tx][ty] > 20 and not isW) or (self.board[tx][ty] > 10 and self.board[tx][ty] < 20 and self.board[tx][ty] != 0 and isW):
				break
			else:
				moves.append(self.coordToStandard(ty, tx))
				if (self.board[tx][ty] > 20 and isW) or (self.board[tx][ty] < 20 and self.board[tx][ty] != 0 and not isW):
					break
		tx = x
		ty = y
		#up right
		while tx-1 >= 0 and ty+1 <= 7:
			tx-=1
			ty+=1
			#black encounter black or white encounter white
			if (self.board[tx][ty] > 20 and not isW) or (self.board[tx][ty] > 10 and self.board[tx][ty] < 20 and self.board[tx][ty] != 0 and isW):
				break
			else:
				moves.append(self.coordToStandard(ty, tx))
				if (self.board[tx][ty] > 20 and isW) or (self.board[tx][ty] < 20 and self.board[tx][ty] != 0 and not isW):
					break
		tx = x
		ty = y
		#up left
		while tx-1 >= 0 and ty-1 >= 0:
			tx-=1
			ty-=1
			#black encounter black or white encounter white
			if (self.board[tx][ty] > 20 and not isW) or (self.board[tx][ty] > 10 and self.board[tx][ty] < 20 and self.board[tx][ty] != 0 and isW):
				break
			else:
				moves.append(self.coordToStandard(ty, tx))
				if (self.board[tx][ty] > 20 and isW) or (self.board[tx][ty] < 20 and self.board[tx][ty] != 0 and not isW):
					break
		tx = x
		ty = y

		return moves

	def getAllRookMoves(self, x, y, isW):	#refactor same as bishop -> only one while
		moves = []
		tx = x
		ty = y

		#down
		while tx+1 <= 7:
			tx += 1
			if (self.board[tx][ty] > 20 and not isW) or (self.board[tx][ty] > 10 and self.board[tx][ty] < 20 and self.board[tx][ty] != 0 and isW):
				break
			else:
				moves.append(self.coordToStandard(ty, tx))
				# and self.board[tx][ty] != 0
				if (self.board[tx][ty] > 20 and isW) or (self.board[tx][ty] < 20 and self.board[tx][ty] != 0 and not isW):
					break
		tx = x
		ty = y
		#right
		while ty+1 <= 7:
			ty += 1
			if (self.board[tx][ty] > 20 and not isW) or (self.board[tx][ty] > 10 and self.board[tx][ty] < 20  and self.board[tx][ty] != 0 and isW):
				break
			else:
				moves.append(self.coordToStandard(ty, tx))
				if (self.board[tx][ty] > 20 and isW) or (self.board[tx][ty] < 20 and self.board[tx][ty] != 0 and not isW):
					break
		tx = x
		ty = y
		#up
		while tx-1 >= 0:
			tx -= 1
			if (self.board[tx][ty] > 20 and not isW) or (self.board[tx][ty] > 10 and self.board[tx][ty] < 20  and self.board[tx][ty] != 0 and isW):
				break
			else:
				moves.append(self.coordToStandard(ty, tx))
				if (self.board[tx][ty] > 20 and isW) or (self.board[tx][ty] < 20 and self.board[tx][ty] != 0 and not isW):
					break
		tx = x
		ty = y
		#left
		while ty-1 >= 0:
			ty -= 1
			if (self.board[tx][ty] > 20 and not isW) or (self.board[tx][ty] > 10 and self.board[tx][ty] < 20  and self.board[tx][ty] != 0 and isW):
				break
			else:
				moves.append(self.coordToStandard(ty, tx))
				if (self.board[tx][ty] > 20 and isW) or (self.board[tx][ty] < 20 and self.board[tx][ty] != 0 and not isW):
					break
		tx = x
		ty = y

		return moves


	def getAllQueenMoves(self, x, y, isW):
		return self.getAllRookMoves(x, y, isW)+self.getAllBishopMoves(x, y, isW)

	def getAllKnightMoves(self, x, y, isW):
		moves = []
		if self.isInBoard(x+2, y-1) and self.isInBoard(x+2, y-1) and (self.board[x+2][y-1] == 0 or (isW and self.isBlackPiece(x+2, y-1)) or not isW and self.isWhitePiece(x+2, y-1)):
			moves.append(self.coordToStandard(y-1, x+2))
		if self.isInBoard(x+2, y+1) and self.isInBoard(x+2, y+1) and (self.board[x+2][y+1] == 0 or (isW and self.isBlackPiece(x+2, y+1)) or not isW and self.isWhitePiece(x+2, y+1)):
			moves.append(self.coordToStandard(y+1, x+2))
		if self.isInBoard(x-2, y-1) and self.isInBoard(x-2, y-1) and (self.board[x-2][y-1] == 0 or (isW and self.isBlackPiece(x-2, y-1)) or not isW and self.isWhitePiece(x-2, y-1)):
			moves.append(self.coordToStandard(y-1, x-2))
		if self.isInBoard(x-2, y+1) and self.isInBoard(x-2, y+1) and (self.board[x-2][y+1] == 0 or (isW and self.isBlackPiece(x-2, y+1)) or not isW and self.isWhitePiece(x-2, y+1)):
			moves.append(self.coordToStandard(y+1, x-2))
		if self.isInBoard(x+1, y-2) and self.isInBoard(x+1, y-2) and (self.board[x+1][y-2] == 0 or (isW and self.isBlackPiece(x+1, y-2)) or not isW and self.isWhitePiece(x+1, y-2)):
			moves.append(self.coordToStandard(y-2, x+1))
		if self.isInBoard(x+1, y+2) and self.isInBoard(x+1, y+2) and (self.board[x+1][y+2] == 0 or (isW and self.isBlackPiece(x+1, y+2)) or not isW and self.isWhitePiece(x+1, y+2)):
			moves.append(self.coordToStandard(y+2, x+1))
		if self.isInBoard(x-1, y-2) and self.isInBoard(x-1, y-2) and (self.board[x-1][y-2] == 0 or (isW and self.isBlackPiece(x-1, y-2)) or not isW and self.isWhitePiece(x-1, y-2)):
			moves.append(self.coordToStandard(y-2, x-1))
		if self.isInBoard(x-1, y+2) and self.isInBoard(x-1, y+2) and (self.board[x-1][y+2] == 0 or (isW and self.isBlackPiece(x-1, y+2)) or not isW and self.isWhitePiece(x-1, y+2)):
			moves.append(self.coordToStandard(y+2, x-1))

		return moves

	def getAllKingMoves(self, x, y, isW):
		moves = []
		if self.isInBoard(x+1, y) and (self.board[x+1][y] == 0 or (isW and self.isBlackPiece(x+1, y)) or not isW and self.isWhitePiece(x+1, y)):
			moves.append(self.coordToStandard(y, x+1))
		if self.isInBoard(x-1, y) and (self.board[x-1][y] == 0 or (isW and self.isBlackPiece(x-1, y)) or not isW and self.isWhitePiece(x-1, y)):
			moves.append(self.coordToStandard(y, x-1))
		if self.isInBoard(x, y+1) and (self.board[x][y+1] == 0 or (isW and self.isBlackPiece(x, y+1)) or not isW and self.isWhitePiece(x, y+1)):
			moves.append(self.coordToStandard(y+1, x))
		if self.isInBoard(x, y-1) and (self.board[x][y-1] == 0 or (isW and self.isBlackPiece(x, y-1)) or not isW and self.isWhitePiece(x, y-1)):
			moves.append(self.coordToStandard(y-1, x))
		if self.isInBoard(x+1, y+1) and (self.board[x+1][y+1] == 0 or (isW and self.isBlackPiece(x+1, y+1)) or not isW and self.isWhitePiece(x+1, y+1)):
			moves.append(self.coordToStandard(y+1, x+1))
		if self.isInBoard(x+1, y-1) and (self.board[x+1][y-1] == 0 or (isW and self.isBlackPiece(x+1, y-1)) or not isW and self.isWhitePiece(x+1, y-1)):
			moves.append(self.coordToStandard(y-1, x+1))
		if self.isInBoard(x-1, y+1) and (self.board[x-1][y+1] == 0 or (isW and self.isBlackPiece(x-1, y+1)) or not isW and self.isWhitePiece(x-1, y+1)):
			moves.append(self.coordToStandard(y+1, x-1))
		if self.isInBoard(x-1, y-1) and (self.board[x-1][y-1] == 0 or (isW and self.isBlackPiece(x-1, y-1)) or not isW and self.isWhitePiece(x-1, y-1)):
			moves.append(self.coordToStandard(y-1, x-1))

		if isW:
			if not self.wKingMoved and x == 7 and y == 4:
				if not self.wRooksMoved[0] and self.board[x][y-1] == 0 and self.board[x][y-2] == 0:
					moves.append(self.coordToStandard(y-2, x))
				if not self.wRooksMoved[1] and self.board[x][y+1] == 0 and self.board[x][y+2] == 0:
					moves.append(self.coordToStandard(y+2, x))
		else:
			if not self.bKingMoved and  x == 0 and y == 4:
				if not self.bRooksMoved[0] and self.board[x][y-1] == 0 and self.board[x][y-2] == 0:
					moves.append(self.coordToStandard(y-2, x))
				if not self.bRooksMoved[1] and self.board[x][y+1] == 0 and self.board[x][y+2] == 0:
					moves.append(self.coordToStandard(y+2, x))



		return moves

	def isCheck(self, tx, ty, moves):
		pass


	#return list of all the possible moves for a position
	def getAllMovesPossible(self, player):
		#ex : { "a1": ["a2", "a3" ...], "c4": ["b3" ...] }
		movesAllowed = {

		}
		a = 0
		if player % 2 != 0:	#to get the correct pieces (if black a = -10)
			a = -10
		for i in range(8):
			for j in range(8):
				p = self.board[i][j]+a
				if p == 11:	#pawn
					movesAllowed[self.coordToStandard(j, i)] = self.getAllPawnMoves(i, j, player % 2 == 0)
				elif p == 13:
					movesAllowed[self.coordToStandard(j, i)] = self.getAllKnightMoves(i, j, player % 2 == 0)
				elif p == 14:
					movesAllowed[self.coordToStandard(j, i)] = self.getAllBishopMoves(i, j, player % 2 == 0)
				elif p == 15:
					movesAllowed[self.coordToStandard(j, i)] = self.getAllRookMoves(i, j, player % 2 == 0)
				elif p == 19:
					movesAllowed[self.coordToStandard(j, i)] = self.getAllQueenMoves(i, j, player % 2 == 0)
				elif p == 12:
					movesAllowed[self.coordToStandard(j, i)] = self.getAllKingMoves(i, j, player % 2 == 0)

	
		"""
		detect a check and trim movesAllowed to the legals moves (to avoid check)
		+++
		>if king under attack from other color
			>try all pos for king color 	(rocks not allowed -> king x+/-2 y== is a rock)
			>if pos result in no check keep 
			>else delete
		
		+++
		if 0 moves possible checkmate (while check)
		if 0 moves possible pat (while not in check)
		"""

		isW = True
		if player % 2 != 0:
			isW = False


		king = self.whereIsKing(isW)
		moves = {

		}
		a = 0
		if player % 2 == 0:	#to get the correct pieces (if black a = -10)
			a = -10
		for i in range(8):
			for j in range(8):
				p = self.board[i][j]+a
				if p == 11:	#pawn
					moves[self.coordToStandard(j, i)] = self.getAllPawnMoves(i, j, player % 2 != 0)
				elif p == 13:
					moves[self.coordToStandard(j, i)] = self.getAllKnightMoves(i, j, player % 2 != 0)
				elif p == 14:
					moves[self.coordToStandard(j, i)] = self.getAllBishopMoves(i, j, player % 2 != 0)
				elif p == 15:
					moves[self.coordToStandard(j, i)] = self.getAllRookMoves(i, j, player % 2 != 0)
				elif p == 19:
					moves[self.coordToStandard(j, i)] = self.getAllQueenMoves(i, j, player % 2 != 0)
				elif p == 12:
					moves[self.coordToStandard(j, i)] = self.getAllKingMoves(i, j, player % 2 != 0)


		#rook / bishop don't work (block it with another piece or take it) 	!!!
		#rock is proposed even when rook is not on board add a 


		"""
		logic:
			keep track of what piece is the attacker
			if one of the tested move is a take of attaker -> add move
			or if one of the tested move is on the path of he attacker (if attacker is rook / bishop / queen)
				store var of a redo of calcul of the piece with new pos (with move that block path)
				if now attacker is still attacking cut move
				else add move (bcs move cut the path to the king)

		"""


		#position check (if case has a rook else rook moved)				!
		if self.isAttacked(king[1], king[0], not isW, moves, self.board):
			b = deepcopy(self.board)
			for key in movesAllowed.keys():
				l = []
				for i in range(len(movesAllowed[key])):
					coord  = self.standardToCoord(key)
					coord2 = self.standardToCoord(movesAllowed[key][i])
					b[coord2[0]][coord2[1]] = b[coord[0]][coord[1]]
					b[coord[0]][coord[1]] = 0
					kingN = self.whereIsKing(isW, b)
					if not self.isAttacked(kingN[1], kingN[0], not isW, moves, b):
						l.append(movesAllowed[key][i])
					b = deepcopy(self.board)
				movesAllowed[key] = l


		return movesAllowed
			

