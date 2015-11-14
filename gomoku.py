import random
import os

#function createBoard:
#--------------------
#Create a grid of size n by n
def createBoard(n):
	#Generate rows with length of n
	board = []
	for row in range(n):
	# Append a blank list to each row cell
		board.append([])
		for column in range(n):
		# Assign x to each row
			board[row].append('X')
	return board

#Create the graphic of the current board
def drawBoard(board):
	# This function prints out the board that it was passed.
	# "board" is a list of 10 strings representing the board (ignore index 0)
	length = len(board)
	for i in range(0, length):
		print('-----------------------')
		for j in range(0, length):
			if j == length - 1:
				print(' ' + board[i][j] + ' ')
			else:
				print(' ' + board[i][j] + ' |'),
	return 0

def runGames():
	print('Welcome to our Gomoku game for CS221')
	while True:
		myBoard = createBoard(5)
		playerOneLetter, playerTwoLetter = ('X', 'O')
		gameIsPlaying = True
		turn = 'playerOne'
		while gameIsPlaying:
			if turn == 'playerOne':
			#Player 1's turn
				drawBoard(myBoard)
			break
		break
	return 0



if __name__ == '__main__':
#      args = readCommand( sys.argv[1:] ) # Get game components based on input
	  runGames()
